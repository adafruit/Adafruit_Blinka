# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Runtime installation helpers for platform-specific dependencies."""

import importlib
import importlib.machinery
import importlib.metadata
import importlib.util
import os
import shlex
import shutil
import subprocess
import sys
import warnings

from packaging.requirements import Requirement
from packaging.version import InvalidVersion

_OPTIONAL_BACKENDS = {
    "_rpi_ws281x",
    "adafruit_raspberry_pi5_neopixel_write",
    "adafruit_blinka_raspberry_pi_pwm",
}


def get_platform_dependencies(detector, python_version=None):
    """Return ``(import name, pip requirement)`` pairs for detected hardware."""
    if python_version is None:
        python_version = sys.version_info[:2]

    # The BCM283x/BCM2711/BCM2712 pin maps share gpiod; PWM no longer depends
    # on either RPi.GPIO or lgpio. NeoPixel support retains its own backend.
    # PWM 1.0.2 permits maintained system gpiod without a transitive upgrade.
    if detector.board.any_raspberry_pi or detector.board.any_raspberry_pi_5_board:
        dependencies = [
            ("gpiod", "gpiod>=2.2.2,<3"),
            (
                "adafruit_blinka_raspberry_pi_pwm",
                "Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2",
            ),
        ]
        if detector.board.any_raspberry_pi_5_board and python_version >= (3, 11):
            dependencies.append(
                (
                    "adafruit_raspberry_pi5_neopixel_write",
                    "Adafruit-Blinka-Raspberry-Pi5-Neopixel",
                )
            )
        elif not detector.board.any_raspberry_pi_5_board:
            dependencies.append(("_rpi_ws281x", "rpi_ws281x>=4.0.0"))
        return dependencies

    if detector.board.any_jetson_board:
        return [("Jetson.GPIO", "Jetson.GPIO")]

    if detector.chip.id == "AM33XX":
        return [("Adafruit_BBIO", "Adafruit_BBIO>=1.2.4")]

    return []


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


def get_missing_platform_dependencies(detector, python_version=None):
    """Return platform requirements whose imports are unavailable or outdated."""
    return [
        requirement
        for module_name, requirement in get_platform_dependencies(
            detector, python_version
        )
        if not _requirement_available(module_name, requirement)
    ]


def get_platform_requirement_for_import(detector, import_name, python_version=None):
    """Return the detected platform's pip requirement for an import name."""
    if detector.board.any_jetson_board and import_name in ("RPi", "RPi.GPIO"):
        # Jetson.GPIO also provides the RPi compatibility namespace used by PWM.
        return "Jetson.GPIO"
    for module_name, requirement in get_platform_dependencies(detector, python_version):
        if import_name in (module_name, module_name.split(".", maxsplit=1)[0]):
            return requirement
    return None


def get_unsupported_platform_dependency_message(
    detector, import_name, python_version=None
):
    """Return guidance when a platform dependency cannot support this Python."""
    if python_version is None:
        python_version = sys.version_info[:2]

    if (
        detector.board.any_raspberry_pi_5_board
        and import_name == "adafruit_raspberry_pi5_neopixel_write"
        and python_version < (3, 11)
    ):
        return (
            "Raspberry Pi 5 NeoPixel support requires Python 3.11 or newer; "
            f"the current interpreter is Python {python_version[0]}.{python_version[1]}."
        )

    return None


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
    """Return installed distributions outside this platform's version bounds."""
    outdated = []
    for module_name, requirement in get_platform_dependencies(detector, python_version):
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


def _raise_for_outdated_dependencies(detector, python_version, optional):
    """Reject unsupported GPIO backends, deferring optional ones to feature use."""
    outdated = [
        requirement
        for requirement in _outdated_platform_dependencies(detector, python_version)
        if requirement not in optional
    ]
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
    """Offer to install missing or outdated dependencies into the environment."""
    if os.environ.get("BLINKA_SKIP_DEPENDENCY_CHECK") == "1":
        return False
    missing = get_missing_platform_dependencies(detector, python_version)
    if not missing:
        return False
    optional = {
        requirement
        for module_name, requirement in get_platform_dependencies(
            detector, python_version
        )
        if module_name in _OPTIONAL_BACKENDS
    }

    if (
        sys.stdin is None
        or sys.stdout is None
        or not (sys.stdin.isatty() and sys.stdout.isatty())
    ):
        _raise_for_outdated_dependencies(detector, python_version, optional)
        return False

    print("\nBlinka detected missing or outdated platform dependencies:")
    for requirement in missing:
        print(f"  - {requirement}")

    try:
        response = input_func(
            "Install them into the current Python environment? [Y/n] "
        )
    except EOFError:
        _raise_for_outdated_dependencies(detector, python_version, optional)
        return False
    if response.strip().lower() not in ("", "y", "yes"):
        _raise_for_outdated_dependencies(detector, python_version, optional)
        return False

    return _install_platform_dependencies(detector, python_version, missing, optional)


def _install_platform_dependencies(detector, python_version, missing, optional):
    """Install confirmed requirements and check same-process usability."""
    if not _pip_available():
        uv_command = shlex.join(
            ["uv", "pip", "install", "--python", sys.executable, *missing]
        )
        message = (
            "The current Python environment has no runnable pip entry point, so Blinka cannot "
            "install its platform dependencies automatically. Install them with "
            "your environment's package manager, or install pip into this "
            f"environment and retry. If using uv, run: {uv_command}\n"
            "Then restart Python before using Blinka."
        )
        if set(missing).issubset(optional):
            warnings.warn(
                message
                + " Blinka startup will continue; optional features may be unavailable.",
                RuntimeWarning,
                stacklevel=2,
            )
            return False
        raise RuntimeError(message)

    # OS-provided modules can be importable without distribution metadata.
    # Any loaded module being installed must be restarted, not just known old ones.
    loaded = [
        module_name
        for module_name, requirement in get_platform_dependencies(
            detector, python_version
        )
        if requirement in missing and sys.modules.get(module_name) is not None
    ]
    command = [sys.executable, "-m", "pip", "install", *missing]
    try:
        subprocess.run(command, check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        install_command = shlex.join(command)
        if set(missing).issubset(optional) and (
            not loaded or isinstance(error, OSError)
        ):
            warnings.warn(
                "Unable to install optional platform dependencies. Blinka startup "
                "will continue; features that need them may be unavailable. "
                f"Try: {install_command}",
                RuntimeWarning,
                stacklevel=2,
            )
            return False
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
        message = (
            "Installation completed, but these platform dependencies are still "
            f"missing or incompatible in this Python process: {', '.join(remaining)}. "
            "Restart Python before using Blinka. If the problem persists, try: "
            f"{install_command}"
        )
        if set(remaining).issubset(optional):
            warnings.warn(message, RuntimeWarning, stacklevel=2)
            return False
        raise RuntimeError(message)
    return True
