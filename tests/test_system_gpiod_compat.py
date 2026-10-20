# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Hardware-free provenance checks for the exceptional Trixie binding build."""

import hashlib
import importlib.machinery
import subprocess
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

from adafruit_blinka import _gpiod_compat as compat

_OTHER_HELPER = (
    "adafruit_blinka_raspberry_pi_pwm._gpiod_compat"
    if compat.__name__ == "adafruit_blinka._gpiod_compat"
    else "adafruit_blinka._gpiod_compat"
)

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name


@pytest.fixture
def system_binding(tmp_path, monkeypatch):  # pylint: disable=too-many-locals
    """Record dpkg responses while retaining real path/checksum operations."""
    site = tmp_path.resolve() / "usr/lib/python3/dist-packages"
    package = site / "gpiod"
    package.mkdir(parents=True)
    metadata = site / "gpiod-2.2.0.dist-info/METADATA"
    metadata.parent.mkdir()
    extension = package / "_ext.so"
    files = {
        package / "__init__.py": b"# maintained binding\n",
        package / "line.py": b"# line enums\n",
        package / "line_request.py": b"# line requests\n",
        package / "chip.py": b"# chip wrapper\n",
        package / "version.py": b'__version__ = "2.2.0"\n',
        extension: b"recording extension; never loaded by the dynamic linker\n",
        metadata: b"Name: gpiod\nVersion: 2.2.0\n",
    }
    for path, contents in files.items():
        path.write_bytes(contents)
    release = tmp_path / "os-release"
    release.write_text('ID=debian\nVERSION_CODENAME="trixie"\n', encoding="utf-8")

    module = ModuleType("gpiod")
    module.__file__ = str(package / "__init__.py")
    module.__version__ = "2.2.0"
    module.__path__ = [str(package)]
    module.__spec__ = importlib.machinery.ModuleSpec(
        "gpiod", None, origin=module.__file__, is_package=True
    )
    module.__spec__.submodule_search_locations = [str(package)]
    module.api_version = "2.2.1"
    native = ModuleType("gpiod._ext")
    native.__file__ = str(extension)
    for name in tuple(sys.modules):
        if name == "gpiod" or name.startswith("gpiod."):
            monkeypatch.delitem(sys.modules, name)
    monkeypatch.delitem(sys.modules, _OTHER_HELPER, raising=False)
    binding_modules = {"gpiod": module, "gpiod._ext": native}
    for submodule in ("line", "line_request", "chip"):
        loaded = ModuleType("gpiod." + submodule)
        loaded.__file__ = str(package / (submodule + ".py"))
        binding_modules["gpiod." + submodule] = loaded
    distribution = SimpleNamespace(
        version="2.2.0", locate_file=lambda name: site / name
    )

    state = SimpleNamespace(
        site=site,
        package=package,
        metadata=metadata,
        extension=extension,
        files=files,
        release=release,
        module=module,
        native=native,
        distribution=distribution,
        binding_modules=binding_modules,
        status="install ok installed\tlibgpiod\t2.2.1-2+deb13u1\n",
        manifest="".join(
            f"{hashlib.md5(contents, usedforsecurity=False).hexdigest()}  "
            f"{str(path).lstrip('/')}\n"
            for path, contents in files.items()
        ),
        error=None,
        calls=[],
        imports=[],
    )

    def run(command, **kwargs):
        state.calls.append((command, kwargs))
        if state.error is not None:
            raise state.error
        output = state.manifest if "--control-show" in command else state.status
        return SimpleNamespace(stdout=output)

    original_import = compat.importlib.import_module

    def import_module(name, *args):
        if name in ("gpiod", "gpiod._ext"):
            state.imports.append(name)
            # File integrity must be checked before importing any binding code.
            assert state.calls and len(state.calls) % 2 == 0
            if name == "gpiod" and name not in sys.modules:
                for module_name, loaded in state.binding_modules.items():
                    monkeypatch.setitem(sys.modules, module_name, loaded)
        return original_import(name, *args)

    original_find_spec = compat.importlib.util.find_spec

    def find_spec(name, *args, **kwargs):
        if name == "gpiod":
            return module.__spec__
        return original_find_spec(name, *args, **kwargs)

    monkeypatch.setattr(compat, "_SYSTEM_SITE", site)
    monkeypatch.setattr(compat, "_OS_RELEASE", release)
    monkeypatch.setattr(compat, "_VERIFIED_MODULES", {})
    monkeypatch.setattr(compat.sys, "platform", "linux")
    monkeypatch.setattr(
        compat.importlib.metadata, "distribution", lambda _: distribution
    )
    monkeypatch.setattr(compat.importlib, "import_module", import_module)
    monkeypatch.setattr(compat.importlib.util, "find_spec", find_spec)
    monkeypatch.setattr(compat.subprocess, "run", run)
    return state


@pytest.mark.parametrize("identity", ["debian", "raspbian"])
def test_accepts_verified_trixie_binding(system_binding, identity):
    system_binding.release.write_text(
        f"ID={identity}\nVERSION_CODENAME=trixie\n", encoding="utf-8"
    )
    assert compat.is_supported_system_gpiod()
    assert system_binding.imports == ["gpiod", "gpiod._ext"]


def test_queries_cannot_be_redirected_by_environment(system_binding, monkeypatch):
    monkeypatch.setenv("DPKG_ROOT", "/untrusted")
    monkeypatch.setenv("DPKG_ADMINDIR", "/untrusted/database")
    assert compat.is_supported_system_gpiod()
    for command, kwargs in system_binding.calls:
        assert command[:4] == [
            "/usr/bin/dpkg-query",
            "--root=/",
            "--admindir=/var/lib/dpkg",
            "--no-pager",
        ]
        assert kwargs["check"]
        assert kwargs["timeout"] == 3
        assert kwargs["stdin"] == subprocess.DEVNULL
        assert kwargs["env"]["LC_ALL"] == "C"


@pytest.mark.parametrize(
    "release",
    [
        "ID=debian\nVERSION_CODENAME=bookworm\n",
        "ID=ubuntu\nVERSION_CODENAME=trixie\n",
        "",
    ],
)
def test_rejects_unknown_os(system_binding, release):
    system_binding.release.write_text(release, encoding="utf-8")
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.calls


def test_rejects_non_linux(system_binding, monkeypatch):
    monkeypatch.setattr(compat.sys, "platform", "darwin")
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.calls


@pytest.mark.parametrize(
    "status",
    [
        "install ok installed\tlibgpiod\t2.2.1-2\n",
        "install ok installed\tlibgpiod\t2.2.2-1\n",
        "install ok installed\tother-package\t2.2.1-2+deb13u1\n",
        "deinstall ok config-files\tlibgpiod\t2.2.1-2+deb13u1\n",
        "",
    ],
)
def test_rejects_unknown_source_or_incomplete_install(system_binding, status):
    system_binding.status = status
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports


@pytest.mark.parametrize(
    "error",
    [
        FileNotFoundError("dpkg-query missing"),
        subprocess.CalledProcessError(2, "dpkg-query"),
        subprocess.TimeoutExpired("dpkg-query", 3),
    ],
)
def test_rejects_dpkg_failure(system_binding, error):
    system_binding.error = error
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports


def test_rejects_pypi_binding_even_with_new_native_api(system_binding):
    system_binding.module.__spec__.origin = (
        "/venv/lib/python3.13/site-packages/gpiod/__init__.py"
    )
    assert system_binding.module.api_version == "2.2.1"
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.calls
    assert not system_binding.imports


def test_rejects_shadowed_distribution(system_binding):
    system_binding.distribution.locate_file = lambda name: Path("/venv") / name
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.calls


def test_rejects_wrong_distribution_version(system_binding):
    system_binding.distribution.version = "2.2.2"
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.calls


@pytest.mark.parametrize("filename", ["__init__.py", "line.py", "_ext.so"])
def test_rejects_modified_binding_file(system_binding, filename):
    (system_binding.package / filename).write_bytes(b"replaced\n")
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports


def test_rejects_modified_metadata(system_binding):
    system_binding.metadata.write_text("Name: modified\n", encoding="utf-8")
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports


@pytest.mark.parametrize("filename", ["line.py", "_ext.so", "METADATA"])
def test_rejects_missing_checksum(system_binding, filename):
    system_binding.manifest = "".join(
        entry + "\n"
        for entry in system_binding.manifest.splitlines()
        if not entry.endswith("/" + filename)
    )
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports


def test_rejects_missing_package_file(system_binding):
    (system_binding.package / "line.py").unlink()
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports


def test_rejects_extra_package_code(system_binding):
    (system_binding.package / "unexpected.py").write_text(
        "# local code\n", encoding="utf-8"
    )
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports


def test_rejects_symlink_to_foreign_binding(system_binding, tmp_path):
    foreign = tmp_path / "foreign.py"
    foreign.write_bytes(system_binding.files[system_binding.package / "line.py"])
    selected = system_binding.package / "line.py"
    selected.unlink()
    selected.symlink_to(foreign)
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports


@pytest.mark.usefixtures("system_binding")
def test_rejects_previously_loaded_foreign_module(monkeypatch):
    foreign = ModuleType("gpiod.line")
    foreign.__file__ = "/venv/gpiod/line.py"
    monkeypatch.setitem(sys.modules, "gpiod.line", foreign)
    assert not compat.is_supported_system_gpiod()


@pytest.mark.parametrize("attribute", ["__file__", "__path__", "__version__"])
def test_rejects_loaded_binding_mismatch(system_binding, attribute):
    value = ["/venv/gpiod"] if attribute == "__path__" else "/venv/gpiod"
    setattr(system_binding.module, attribute, value)
    assert not compat.is_supported_system_gpiod()


def test_rejects_loaded_extension_mismatch(system_binding):
    system_binding.native.__file__ = "/venv/gpiod/_ext.so"
    assert not compat.is_supported_system_gpiod()


def test_rejects_unexpected_native_version(system_binding):
    system_binding.module.api_version = "2.1.3"
    assert not compat.is_supported_system_gpiod()


def test_native_api_version_is_a_string_not_a_function(system_binding):
    """Official bindings expose _ext.api_version with PyModule_AddStringConstant."""
    assert isinstance(system_binding.module.api_version, str)
    assert compat.is_supported_system_gpiod()
    system_binding.calls.clear()
    system_binding.module.api_version = lambda: "2.2.1"
    assert not compat.is_supported_system_gpiod()


def test_does_not_cache_success_across_file_changes(system_binding):
    assert compat.is_supported_system_gpiod()
    system_binding.calls.clear()
    system_binding.extension.write_bytes(b"different binding\n")
    assert not compat.is_supported_system_gpiod()


@pytest.mark.parametrize("submodule", ["chip", "line_request"])
def test_rejects_same_path_stale_module_after_os_reinstall(
    system_binding, monkeypatch, submodule
):
    """Restored files cannot attest code objects loaded before the repair."""
    module_name = "gpiod." + submodule
    stale = ModuleType(module_name)
    path = system_binding.package / (submodule + ".py")
    stale.__file__ = str(path)
    path.write_bytes(b"# previously edited code\n")
    monkeypatch.setitem(sys.modules, module_name, stale)
    path.write_bytes(system_binding.files[path])
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports


def test_rechecks_files_but_accepts_verified_repeat(system_binding):
    assert compat.is_supported_system_gpiod()
    first_objects = dict(compat._VERIFIED_MODULES)  # pylint: disable=protected-access
    system_binding.calls.clear()
    assert compat.is_supported_system_gpiod()
    assert len(system_binding.calls) == 2
    assert all(sys.modules[name] is loaded for name, loaded in first_objects.items())


@pytest.mark.parametrize("mirror_first", [False, True])
def test_mirrored_helpers_share_identity_attestations(
    system_binding, monkeypatch, mirror_first
):
    spec = importlib.util.spec_from_file_location(_OTHER_HELPER, compat.__file__)
    mirror = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, _OTHER_HELPER, mirror)
    spec.loader.exec_module(mirror)
    monkeypatch.setattr(mirror, "_SYSTEM_SITE", system_binding.site)
    monkeypatch.setattr(mirror, "_OS_RELEASE", system_binding.release)
    first, second = (mirror, compat) if mirror_first else (compat, mirror)
    assert first.is_supported_system_gpiod()
    system_binding.calls.clear()
    assert second.is_supported_system_gpiod()
    assert len(system_binding.calls) == 2


@pytest.mark.parametrize("module_name", ["gpiod", "gpiod.line_request", "gpiod.chip"])
def test_rejects_replaced_previously_verified_object(
    system_binding, monkeypatch, module_name
):
    assert compat.is_supported_system_gpiod()
    replacement = ModuleType(module_name)
    replacement.__file__ = sys.modules[module_name].__file__
    monkeypatch.setitem(sys.modules, module_name, replacement)
    system_binding.calls.clear()
    system_binding.imports.clear()
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports


def test_rejects_new_same_path_submodule_after_verification(
    system_binding, monkeypatch
):
    assert compat.is_supported_system_gpiod()
    # version.py was checked on disk, but this later object has no provenance.
    unexpected = ModuleType("gpiod.version")
    unexpected.__file__ = str(system_binding.package / "version.py")
    monkeypatch.setitem(sys.modules, "gpiod.version", unexpected)
    system_binding.calls.clear()
    system_binding.imports.clear()
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports


def test_identity_attestation_does_not_cache_package_status(system_binding):
    assert compat.is_supported_system_gpiod()
    system_binding.calls.clear()
    system_binding.status = "install ok installed\tlibgpiod\t2.2.2-1\n"
    assert not compat.is_supported_system_gpiod()
    assert len(system_binding.calls) == 1


def test_failed_validation_does_not_attest_imported_objects(system_binding):
    system_binding.module.api_version = "unexpected"
    assert not compat.is_supported_system_gpiod()
    system_binding.module.api_version = "2.2.1"
    system_binding.calls.clear()
    system_binding.imports.clear()
    assert not compat.is_supported_system_gpiod()
    assert not system_binding.imports
