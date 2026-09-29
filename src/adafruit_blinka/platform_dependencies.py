# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Runtime installation helpers for platform-specific dependencies."""

import importlib
import importlib.util
import shlex
import subprocess
import sys


def get_platform_dependencies(detector, python_version=None):
    """Return ``(import name, pip requirement)`` pairs for detected hardware."""
    if python_version is None:
        python_version = sys.version_info[:2]

    # BCM2712 is currently the only Blinka microcontroller backend that imports
    # generic_linux.lgpio_pin or generic_linux.lgpio_pwmout. Keep lgpio scoped
    # to that backend rather than installing it for Raspberry Pi generally.
    if detector.board.any_raspberry_pi_5_board:
        lgpio_requirement = (
            "adafruit-lgpio>=0.2.2.0" if python_version >= (3, 13) else "lgpio>=0.2.2.0"
        )
        dependencies = [("lgpio", lgpio_requirement)]
        if python_version >= (3, 11):
            dependencies.append(
                (
                    "adafruit_raspberry_pi5_neopixel_write",
                    "Adafruit-Blinka-Raspberry-Pi5-Neopixel",
                )
            )
        return dependencies

    if detector.board.any_raspberry_pi:
        return [
            ("RPi.GPIO", "RPi.GPIO"),
            ("_rpi_ws281x", "rpi_ws281x>=4.0.0"),
        ]

    if detector.board.any_jetson_board:
        return [("Jetson.GPIO", "Jetson.GPIO")]

    if detector.chip.id == "AM33XX":
        return [("Adafruit_BBIO", "Adafruit_BBIO>=1.2.4")]

    return []


def _module_available(module_name):
    """Return whether an import can be resolved without importing the module."""
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ImportError, ModuleNotFoundError):
        return False


def get_missing_platform_dependencies(detector, python_version=None):
    """Return platform requirements whose import modules are unavailable."""
    return [
        requirement
        for module_name, requirement in get_platform_dependencies(
            detector, python_version
        )
        if not _module_available(module_name)
    ]


def get_platform_requirement_for_import(detector, import_name, python_version=None):
    """Return the detected platform's pip requirement for an import name."""
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


def format_install_command(requirements, executable="pip"):
    """Return a shell-safe command for installing pip requirements."""
    if executable == "pip":
        command = [executable, "install", *requirements]
    else:
        command = [executable, "-m", "pip", "install", *requirements]
    return shlex.join(command)


def install_missing_platform_dependencies(
    detector, python_version=None, input_func=input
):
    """Offer to install missing dependencies into the running Python environment."""
    missing = get_missing_platform_dependencies(detector, python_version)
    if not missing:
        return False

    if (
        sys.stdin is None
        or sys.stdout is None
        or not (sys.stdin.isatty() and sys.stdout.isatty())
    ):
        return False

    print("\nBlinka detected missing platform dependencies:")
    for requirement in missing:
        print(f"  - {requirement}")

    try:
        response = input_func(
            "Install them into the current Python environment? [Y/n] "
        )
    except EOFError:
        return False
    if response.strip().lower() not in ("", "y", "yes"):
        return False

    command = [sys.executable, "-m", "pip", "install", *missing]
    try:
        subprocess.run(command, check=True)
    except (OSError, subprocess.CalledProcessError) as error:
        install_command = shlex.join(command)
        raise RuntimeError(
            f"Unable to install the platform dependencies. Try: {install_command}"
        ) from error

    importlib.invalidate_caches()
    return True
