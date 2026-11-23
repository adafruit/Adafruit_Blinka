# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Runtime installation helpers for platform-specific dependencies."""

import importlib
import importlib.machinery
import importlib.metadata
import importlib.util
import json
import os
import shlex
import shutil
import subprocess
import sys
from functools import lru_cache
from importlib.resources import files

from packaging.requirements import Requirement
from packaging.version import InvalidVersion


@lru_cache(maxsize=1)
def _registry():
    """Read the bundled dependency declarations only when needed."""
    resource = files("adafruit_blinka").joinpath("platform_dependencies.json")
    return json.loads(resource.read_text(encoding="utf-8"))


def _platform_packages(detector):
    """Yield the ordered packages for the first matching platform rule."""
    registry = _registry()
    for platform in registry["platforms"]:
        if _matches_platform(detector, platform):
            for name in platform["packages"]:
                yield name, registry["packages"][name]
            return


def _matches_platform(detector, platform):
    if "board" in platform:
        return getattr(detector.board, platform["board"])
    return detector.chip.id == platform["chip"]


def _python_is_supported(package, python_version):
    return python_version >= tuple(package.get("minimum_python", ()))


def _platform_dependencies(detector, python_version):
    """Yield supported package records, without probing installed libraries."""
    if python_version is None:
        python_version = sys.version_info[:2]
    for name, package in _platform_packages(detector):
        if _python_is_supported(package, python_version):
            yield name, package


def get_platform_dependencies(detector, python_version=None):
    """Return ``(import name, pip requirement)`` pairs for detected hardware."""
    return [
        (name, package["requirement"])
        for name, package in _platform_dependencies(detector, python_version)
    ]


def _installed_version_supported(module_name, requirement, installed_version):
    """Check normal version bounds or maintained system gpiod bindings."""
    try:
        supported = requirement.specifier.contains(installed_version, prereleases=True)
        if module_name == "gpiod" and sys.modules.get("gpiod") is not None:
            # Replacing files cannot upgrade an already loaded native binding.
            supported = supported and requirement.specifier.contains(
                getattr(sys.modules["gpiod"], "__version__", ""), prereleases=True
            )
    except (InvalidVersion, TypeError):
        supported = False
    if (
        supported
        or module_name != "gpiod"
        or installed_version != "2.2.0"
        or not requirement.specifier.contains("2.2.2", prereleases=True)
    ):
        return supported

    # Maintained distro bindings retain a label shared with buggy PyPI 2.2.0.
    # Check their system-package origin and source/native versions instead.
    from ._gpiod_compat import is_supported_system_gpiod

    return is_supported_system_gpiod()


def _requirement_available(module_name, requirement):
    """Return whether an import and its required distribution version are available."""
    try:
        if importlib.util.find_spec(module_name) is None:
            return False
    except (ImportError, ModuleNotFoundError):
        return False

    parsed_requirement = Requirement(requirement)
    if not parsed_requirement.specifier:
        return True

    try:
        installed_version = importlib.metadata.version(parsed_requirement.name)
    except importlib.metadata.PackageNotFoundError:
        return False

    return _installed_version_supported(
        module_name, parsed_requirement, installed_version
    )


def _required_platform_dependencies(detector, python_version):
    """Yield only the dependencies checked and installed at board startup."""
    packages = _registry()["packages"]
    for module_name, requirement in get_platform_dependencies(detector, python_version):
        if not packages.get(module_name, {}).get("optional", False):
            yield module_name, requirement


def get_missing_platform_dependencies(detector, python_version=None):
    """Return required platform dependencies that are unavailable or outdated."""
    return [
        requirement
        for module_name, requirement in _required_platform_dependencies(
            detector, python_version
        )
        if not _requirement_available(module_name, requirement)
    ]


def get_platform_requirement_for_import(detector, import_name, python_version=None):
    """Return the detected platform's pip requirement for an import name."""
    if python_version is None:
        python_version = sys.version_info[:2]
    registry = _registry()
    # Compatibility namespaces (such as RPi on Jetson) are not startup checks.
    for platform in registry["platforms"]:
        alias = platform.get("aliases", {}).get(import_name)
        if alias is not None and _matches_platform(detector, platform):
            package = registry["packages"][alias]
            if _python_is_supported(package, python_version):
                return package["requirement"]

    for name, package in _platform_dependencies(detector, python_version):
        if import_name in (name, name.split(".", maxsplit=1)[0]):
            return package["requirement"]
    return None


def get_unsupported_platform_dependency_message(
    detector, import_name, python_version=None
):
    """Return guidance when a platform dependency cannot support this Python."""
    if python_version is None:
        python_version = sys.version_info[:2]

    registry = _registry()
    package = registry["packages"].get(import_name)
    if package is None or _python_is_supported(package, python_version):
        return None
    # Don't probe unrelated board rules just to check one feature's Python floor.
    if not any(
        import_name in platform["packages"] and _matches_platform(detector, platform)
        for platform in registry["platforms"]
    ):
        return None

    minimum = ".".join(map(str, package["minimum_python"]))
    current = ".".join(map(str, python_version[:2]))
    return (
        f"{package['feature']} requires Python {minimum} or newer; "
        f"the current interpreter is Python {current}."
    )


def _pip_available():
    """Find this interpreter's pip entry point without importing or executing it."""
    try:
        spec = importlib.util.find_spec("pip")
        if spec is not None and spec.submodule_search_locations is not None:
            # Dotted util.find_spec would import pip. Search its package paths
            # directly instead, including namespace leftovers from uninstalling.
            spec = importlib.machinery.PathFinder.find_spec(
                "pip.__main__", spec.submodule_search_locations
            )
        return (
            spec is not None
            and spec.loader is not None
            and spec.submodule_search_locations is None
        )
    except (ImportError, AttributeError, KeyError, TypeError, ValueError):
        return False


def format_install_command(requirements, executable="pip"):
    """Return shell-safe manual installation guidance for the target Python."""
    if executable == "pip":
        command = [executable, "install", *requirements]
    else:
        command = [executable, "-m", "pip", "install", *requirements]
        if executable == sys.executable and not _pip_available():
            if shutil.which("uv") is not None:
                command = [
                    "uv",
                    "pip",
                    "install",
                    "--python",
                    executable,
                    *requirements,
                ]
    return shlex.join(command)


def check_platform_dependency(detector, import_name, python_version=None):
    """Check a backend when its feature is imported, without installing it."""
    unsupported = get_unsupported_platform_dependency_message(
        detector, import_name, python_version
    )
    if unsupported is not None:
        raise RuntimeError(unsupported)

    requirement = get_platform_requirement_for_import(
        detector, import_name, python_version
    )
    if requirement is None:
        return
    parsed = Requirement(requirement)
    if not parsed.specifier:
        return
    try:
        installed_version = importlib.metadata.version(parsed.name)
    except importlib.metadata.PackageNotFoundError:
        # Let the backend import report missing modules; OS packages may have
        # no Python distribution metadata at all.
        return
    if not _installed_version_supported(import_name, parsed, installed_version):
        install_command = format_install_command([requirement], sys.executable)
        raise RuntimeError(
            f"The platform library '{import_name}' has unsupported installed version "
            f"{installed_version}. To install a supported version, run: "
            f"{install_command}\nThen restart Python before using this feature."
        )


def _outdated_platform_dependencies(detector, python_version):
    """Return installed required distributions with unsupported versions."""
    outdated = []
    for module_name, requirement in _required_platform_dependencies(
        detector, python_version
    ):
        parsed_requirement = Requirement(requirement)
        if not parsed_requirement.specifier:
            continue
        try:
            installed_version = importlib.metadata.version(parsed_requirement.name)
        except importlib.metadata.PackageNotFoundError:
            continue
        if not _installed_version_supported(
            module_name, parsed_requirement, installed_version
        ):
            outdated.append(requirement)
    return outdated


def _raise_for_outdated_dependencies(detector, python_version):
    """Reject unsupported required dependencies."""
    outdated = _outdated_platform_dependencies(detector, python_version)
    if outdated:
        install_command = format_install_command(outdated, executable=sys.executable)
        raise RuntimeError(
            "Blinka found installed platform dependencies with unsupported versions. "
            f"To install supported versions, run: {install_command}\n"
            "Then restart Python before using Blinka."
        )


def install_missing_platform_dependencies(
    detector, python_version=None, input_func=input
):
    """Offer to install missing or outdated required dependencies."""
    if os.environ.get("BLINKA_SKIP_DEPENDENCY_CHECK") == "1":
        return False
    missing = get_missing_platform_dependencies(detector, python_version)
    if not missing:
        return False
    if (
        sys.stdin is None
        or sys.stdout is None
        or not (sys.stdin.isatty() and sys.stdout.isatty())
    ):
        _raise_for_outdated_dependencies(detector, python_version)
        return False

    print("\nBlinka detected missing or outdated required platform dependencies:")
    for requirement in missing:
        print(f"  - {requirement}")

    try:
        response = input_func(
            "Install them into the current Python environment? [Y/n] "
        )
    except EOFError:
        _raise_for_outdated_dependencies(detector, python_version)
        return False
    if response.strip().lower() not in ("", "y", "yes"):
        _raise_for_outdated_dependencies(detector, python_version)
        return False

    return _install_platform_dependencies(detector, python_version, missing)


def _install_platform_dependencies(detector, python_version, missing):
    """Install confirmed requirements and check same-process usability."""
    if not _pip_available():
        uv_command = shlex.join(
            ["uv", "pip", "install", "--python", sys.executable, *missing]
        )
        raise RuntimeError(
            "The current Python environment has no runnable pip entry point, so Blinka cannot "
            "install its platform dependencies automatically. Install them with "
            "your environment's package manager, or install pip into this "
            f"environment and retry. If using uv, run: {uv_command}\n"
            "Then restart Python before using Blinka."
        )

    # OS-provided modules can be importable without distribution metadata.
    # Any loaded module being installed must be restarted, not just known old ones.
    loaded = [
        module_name
        for module_name, requirement in _required_platform_dependencies(
            detector, python_version
        )
        if requirement in missing and sys.modules.get(module_name) is not None
    ]
    command = [sys.executable, "-m", "pip", "install", *missing]
    try:
        subprocess.run(command, check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        install_command = shlex.join(command)
        raise RuntimeError(
            f"Unable to install the platform dependencies. Try: {install_command}"
        ) from error

    importlib.invalidate_caches()
    if loaded:
        raise RuntimeError(
            "The platform dependencies were installed, but these modules were already "
            f"loaded: {', '.join(loaded)}. Restart Python before using Blinka."
        )
    remaining = get_missing_platform_dependencies(detector, python_version)
    if remaining:
        install_command = format_install_command(remaining, executable=sys.executable)
        raise RuntimeError(
            "Installation completed, but these platform dependencies are still "
            f"missing or incompatible in this Python process: {', '.join(remaining)}. "
            "Restart Python before using Blinka. If the problem persists, try: "
            f"{install_command}"
        )
    return True
