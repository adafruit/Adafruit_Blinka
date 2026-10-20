# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Hardware-free checks for the maintained system binding version exception."""

import subprocess
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

from adafruit_blinka import _gpiod_compat as compat

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name,protected-access


@pytest.fixture
def system_binding(tmp_path, monkeypatch):  # pylint: disable=too-many-locals
    """Supply real selected paths, recording modules, and one dpkg response."""
    site = tmp_path.resolve() / "usr/lib/python3/dist-packages"
    package = site / "gpiod"
    package.mkdir(parents=True)
    metadata = site / "gpiod-2.2.0.dist-info/METADATA"
    metadata.parent.mkdir()
    extension = package / "_ext.cpython-313-aarch64-linux-gnu.so"
    for path in (package / "__init__.py", metadata, extension):
        path.write_text("# maintained system package\n", encoding="utf-8")
    metadata.write_text("Name: gpiod\nVersion: 2.2.0\n", encoding="utf-8")

    def forbidden_gpio(*_args, **_kwargs):
        pytest.fail("compatibility detection must not open/request GPIOs")

    module = ModuleType("gpiod")
    module.__file__ = str(package / "__init__.py")
    module.__version__ = "2.2.0"
    module.__path__ = [str(package)]
    module.Chip = forbidden_gpio
    module.request_lines = forbidden_gpio
    native = ModuleType("gpiod._ext")
    native.__file__ = str(extension)
    native.api_version = "2.2.1"
    native.Chip = forbidden_gpio
    for name in tuple(sys.modules):
        if name == "gpiod" or name.startswith("gpiod."):
            monkeypatch.delitem(sys.modules, name)
    distribution = SimpleNamespace(
        version="2.2.0", locate_file=lambda name: site / name, _path=metadata.parent
    )
    state = SimpleNamespace(
        site=site,
        package=package,
        metadata=metadata,
        extension=extension,
        module=module,
        native=native,
        distribution=distribution,
        status="install ok installed\tlibgpiod\t2.2.1",
        owned={package / "__init__.py", extension, metadata},
        error=None,
        calls=[],
        imports=[],
    )

    def run(command, **kwargs):
        state.calls.append((command, kwargs))
        if state.error is not None:
            raise state.error
        return SimpleNamespace(
            stdout=state.status + "\n" + "\n".join(str(path) for path in state.owned)
        )

    original_import = compat.importlib.import_module

    def import_module(name, *args):
        if name in ("gpiod", "gpiod._ext"):
            state.imports.append(name)
            selected = module if name == "gpiod" else native
            if name not in sys.modules:
                monkeypatch.setitem(sys.modules, name, selected)
        return original_import(name, *args)

    compat._system_package_files.cache_clear()
    monkeypatch.setattr(compat, "_SYSTEM_SITE", site)
    monkeypatch.setattr(compat.sys, "platform", "linux")
    monkeypatch.setattr(
        compat.importlib.metadata, "distribution", lambda _: distribution
    )
    monkeypatch.setattr(compat.importlib, "import_module", import_module)
    monkeypatch.setattr(compat.subprocess, "run", run)
    yield state
    compat._system_package_files.cache_clear()


def test_accepts_maintained_binding_without_gpio_access(system_binding):
    """Importing and identifying the binding never constructs a GPIO object."""
    assert compat.is_supported_system_gpiod()
    assert system_binding.imports == ["gpiod", "gpiod._ext"]
    assert len(system_binding.calls) == 1


def test_accepts_preloaded_system_bindings(system_binding, monkeypatch):
    """Ordinary raw-gpiod-first and Blinka-first import orders are supported."""
    monkeypatch.setitem(sys.modules, "gpiod", system_binding.module)
    monkeypatch.setitem(sys.modules, "gpiod._ext", system_binding.native)
    assert compat.is_supported_system_gpiod()


def test_accepts_actual_system_metadata_directory(system_binding, monkeypatch):
    """Check the real stdlib distribution's origin, not a constructed path."""
    distribution = compat.importlib.metadata.PathDistribution(
        system_binding.metadata.parent
    )
    monkeypatch.setattr(
        compat.importlib.metadata, "distribution", lambda _name: distribution
    )
    assert distribution.version == "2.2.0"
    assert compat.is_supported_system_gpiod()


def test_rejects_unowned_selected_metadata_in_same_system_root(
    system_binding, monkeypatch
):
    """Another metadata directory shares locate_file's root but not ownership."""
    selected = system_binding.site / "gpiod-2.2.0.egg-info"
    selected.mkdir()
    (selected / "PKG-INFO").write_text(
        "Name: gpiod\nVersion: 2.2.0\n", encoding="utf-8"
    )
    distribution = compat.importlib.metadata.PathDistribution(selected)
    monkeypatch.setattr(
        compat.importlib.metadata, "distribution", lambda _name: distribution
    )
    assert distribution.version == "2.2.0"
    assert distribution.locate_file("") == system_binding.site
    assert not compat.is_supported_system_gpiod()


def test_rejects_distribution_without_metadata_origin(system_binding):
    """An unavailable concrete metadata origin cannot qualify for the exception."""
    del system_binding.distribution._path
    assert not compat.is_supported_system_gpiod()


@pytest.mark.parametrize("upstream", ["2.2.1", "2.2.2", "2.3", "2.9.1"])
def test_accepts_maintained_upstreams_and_any_debian_revision(system_binding, upstream):
    """Package maintenance updates do not depend on an exact distro revision."""
    # source:Upstream-Version excludes deb13u1/deb13u2 and binary rebuild suffixes.
    system_binding.status = "install ok installed\tlibgpiod\t" + upstream
    assert compat.is_supported_system_gpiod()
    command = system_binding.calls[0][0]
    assert "${source:Upstream-Version}" in command[-2]
    assert "${source:Version}" not in command[-2]


@pytest.mark.parametrize(
    "status",
    [
        "install ok installed\tlibgpiod\t2.2.0",
        "install ok installed\tlibgpiod\t2.2.1rc1",
        "install ok installed\tlibgpiod\t2.3rc1",
        "install ok installed\tlibgpiod\t3.0",
        "install ok installed\tlibgpiod\tinvalid",
        "install ok installed\tother-package\t2.2.1",
        "deinstall ok config-files\tlibgpiod\t2.2.1",
        "",
        "install ok installed\tlibgpiod",
    ],
)
def test_rejects_unsafe_source_or_incomplete_install(system_binding, status):
    """Only fully installed maintained libgpiod source builds qualify."""
    system_binding.status = status
    assert not compat.is_supported_system_gpiod()


@pytest.mark.parametrize("filename", ["__init__.py", "_ext", "METADATA"])
def test_requires_selected_files_to_be_package_owned(system_binding, filename):
    """Both Python/native binding code and its metadata must be OS-managed."""
    selected = {
        "__init__.py": system_binding.package / "__init__.py",
        "_ext": system_binding.extension,
        "METADATA": system_binding.metadata,
    }[filename]
    system_binding.owned.remove(selected)
    assert not compat.is_supported_system_gpiod()


@pytest.mark.parametrize("selected", ["module", "extension", "metadata"])
def test_rejects_pypi_paths_even_with_new_native_version(system_binding, selected):
    """Linking buggy PyPI Python code to fixed native libgpiod is not enough."""
    if selected == "module":
        system_binding.module.__file__ = (
            "/venv/lib/python3.13/site-packages/gpiod/__init__.py"
        )
    elif selected == "extension":
        system_binding.native.__file__ = (
            "/venv/lib/python3.13/site-packages/gpiod/_ext.so"
        )
    else:
        system_binding.distribution.locate_file = lambda name: Path("/venv") / name
    assert system_binding.native.api_version == "2.2.1"
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.calls


def test_rejects_shadowed_package_search_path(system_binding):
    """Do not combine system Python bindings with a shadow package directory."""
    system_binding.module.__path__ = ["/venv/gpiod", str(system_binding.package)]
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.calls


@pytest.mark.parametrize("attribute", ["module", "metadata"])
def test_exception_requires_both_python_labels_220(system_binding, attribute):
    """Other Python release labels belong to callers' ordinary version checks."""
    if attribute == "module":
        system_binding.module.__version__ = "2.2.2"
    else:
        system_binding.distribution.version = "2.2.2"
    assert not compat.is_supported_system_gpiod()


@pytest.mark.parametrize("version", ["2.2.0", "2.1.3", "3.0", "2.2.1rc1", "bad"])
def test_rejects_old_or_unusable_loaded_native_version(system_binding, version):
    """Reject incompatible loaded native libraries despite a maintained package."""
    system_binding.native.api_version = version
    assert not compat.is_supported_system_gpiod()


def test_rejects_old_loaded_native_despite_cached_new_package(system_binding):
    """Caching OS facts does not suppress the cheap loaded-library version check."""
    assert compat.is_supported_system_gpiod()
    system_binding.native.api_version = "2.2.0"
    assert not compat.is_supported_system_gpiod()
    assert len(system_binding.calls) == 1


def test_native_api_version_is_a_string_not_a_function(system_binding):
    """Official bindings expose the native version as a string constant."""
    system_binding.native.api_version = lambda: "2.2.1"
    assert not compat.is_supported_system_gpiod()


def test_rechecks_selected_paths_but_caches_package_query(system_binding):
    """Repeated PWM construction queries dpkg once but still detects shadowing."""
    assert compat.is_supported_system_gpiod()
    assert compat.is_supported_system_gpiod()
    assert len(system_binding.calls) == 1
    system_binding.module.__file__ = "/venv/gpiod/__init__.py"
    assert not compat.is_supported_system_gpiod()
    assert len(system_binding.calls) == 1


@pytest.mark.parametrize(
    "error",
    [
        FileNotFoundError("dpkg-query missing"),
        subprocess.CalledProcessError(2, "dpkg-query"),
        subprocess.TimeoutExpired("dpkg-query", 3),
    ],
)
def test_caches_dpkg_failures_without_accepting_binding(system_binding, error):
    """Unavailable package information remains a refusal until Python restarts."""
    system_binding.error = error
    assert not compat.is_supported_system_gpiod()
    system_binding.error = None
    assert not compat.is_supported_system_gpiod()
    assert len(system_binding.calls) == 1


def test_package_upgrade_requires_process_restart(system_binding):
    """Package database changes become visible in a fresh interpreter process."""
    system_binding.status = "install ok installed\tlibgpiod\t2.2.0"
    assert not compat.is_supported_system_gpiod()
    system_binding.status = "install ok installed\tlibgpiod\t2.2.1"
    assert not compat.is_supported_system_gpiod()
    compat._system_package_files.cache_clear()  # Represents a fresh Python process.
    assert compat.is_supported_system_gpiod()


def test_queries_cannot_be_redirected_by_environment(system_binding, monkeypatch):
    """Check the real OS database with stable output and a bounded timeout."""
    monkeypatch.setenv("DPKG_ROOT", "/untrusted")
    monkeypatch.setenv("DPKG_ADMINDIR", "/untrusted/database")
    assert compat.is_supported_system_gpiod()
    command, kwargs = system_binding.calls[0]
    assert command[:5] == [
        "/usr/bin/dpkg-query",
        "--root=/",
        "--admindir=/var/lib/dpkg",
        "--no-pager",
        "--show",
    ]
    assert command[-1] == "python3-libgpiod"
    assert kwargs["check"]
    assert kwargs["timeout"] == 3
    assert kwargs["stdin"] == subprocess.DEVNULL
    assert kwargs["env"]["LC_ALL"] == "C"
    assert kwargs["env"]["LANGUAGE"] == "C"


def test_rejects_non_linux_without_imports(system_binding, monkeypatch):
    """The system-package exception is Linux-only."""
    monkeypatch.setattr(compat.sys, "platform", "darwin")
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports
    assert not system_binding.calls


@pytest.mark.parametrize("filename", ["__init__.py", "_ext", "METADATA"])
def test_rejects_symlinks_to_another_install(system_binding, tmp_path, filename):
    """Package filenames must not resolve into a different installation."""
    selected = {
        "__init__.py": system_binding.package / "__init__.py",
        "_ext": system_binding.extension,
        "METADATA": system_binding.metadata,
    }[filename]
    foreign = tmp_path / "foreign-file"
    foreign.write_text("# different installation\n", encoding="utf-8")
    selected.unlink()
    selected.symlink_to(foreign)
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.calls


@pytest.mark.usefixtures("system_binding")
def test_rejects_missing_module_or_metadata_without_raising(monkeypatch):
    """Missing distribution metadata is not an unrelated startup exception."""

    def missing(_name):
        raise compat.importlib.metadata.PackageNotFoundError("gpiod")

    monkeypatch.setattr(compat.importlib.metadata, "distribution", missing)
    assert not compat.is_supported_system_gpiod()


def test_rejects_missing_selected_file_without_raising(system_binding):
    """Missing selected native code cannot qualify as an OS-maintained binding."""
    system_binding.extension.unlink()
    assert not compat.is_supported_system_gpiod()
