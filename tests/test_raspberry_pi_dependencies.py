# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Packaging and import diagnostics without importing any GPIO library."""

# Pytest provides the named monkeypatch fixture.
# pylint: disable=redefined-outer-name

import builtins
import importlib.util
import io
import os
import runpy
import sys
from collections import namedtuple
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).parents[1]
COMPATIBLE = "/proc/device-tree/compatible"
PI_REQUIREMENTS = {
    "rpi_ws281x>=4.0.0",
    "Adafruit-Blinka-Raspberry-Pi5-Neopixel",
}
NATIVE_SPECIFIERS = {
    "gpiod": "<3,>=2.2.2",
    "adafruit-blinka-raspberry-pi-pwm": ">=1.0.1",
}
ARM_MARKER_CASES = [
    ("linux", "armv6l", True),
    ("linux", "armv7l", True),
    ("linux", "aarch64", True),
    ("linux", "x86_64", False),
    ("darwin", "arm64", False),
    ("win32", "AMD64", False),
    ("darwin", "aarch64", False),
    ("win32", "aarch64", False),
]
PI_COMPATIBLES = [
    b"brcm,bcm2835",
    b"brcm,bcm2836",
    b"brcm,bcm2837",
    b"brcm,bcm2838",
    b"brcm,bcm2711",
    b"brcm,bcm2712",
]
GPIO_MODULES = {"gpiod", "lgpio", "RPi", "adafruit_blinka_raspberry_pi_pwm"}
VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")


def setup_metadata(monkeypatch, compatible, python_minor=12):
    """Capture setup() while faking only board detection and package discovery."""
    captured = {}
    setuptools = ModuleType("setuptools")
    setuptools.setup = lambda **kwargs: captured.update(kwargs)
    setuptools.find_packages = lambda _directory: []
    original_exists = os.path.exists
    original_open = builtins.open
    original_import = builtins.__import__

    def exists(path):
        if os.fspath(path) == COMPATIBLE:
            return compatible is not None
        return original_exists(path)

    def open_compatible(path, *args, **kwargs):
        if os.fspath(path) == COMPATIBLE:
            assert compatible is not None
            assert args == ("rb",)
            return io.BytesIO(compatible)
        return original_open(path, *args, **kwargs)

    def import_without_gpio(name, *args, **kwargs):
        assert name.split(".")[0] not in GPIO_MODULES
        return original_import(name, *args, **kwargs)

    with monkeypatch.context() as patches:
        patches.setitem(sys.modules, "setuptools", setuptools)
        patches.setattr(os.path, "exists", exists)
        patches.setattr(builtins, "open", open_compatible)
        patches.setattr(builtins, "__import__", import_without_gpio)
        patches.setattr(
            sys, "version_info", VersionInfo(3, python_minor, 0, "final", 0)
        )
        runpy.run_path(str(ROOT / "setup.py"), run_name="__main__")
    return captured


@pytest.mark.parametrize("python_minor", [9, 12, 13])
@pytest.mark.parametrize("compatible", PI_COMPATIBLES)
def test_pi_setup_dependencies(monkeypatch, compatible, python_minor):
    """Every supported Pi chip receives the same new GPIO/PWM dependencies."""
    metadata = setup_metadata(monkeypatch, compatible, python_minor)
    requirements = set(metadata["install_requires"])
    baseline = set(setup_metadata(monkeypatch, None, python_minor)["install_requires"])
    assert requirements == baseline | PI_REQUIREMENTS
    parsed = parse_requirements(requirements)
    assert set(parsed).isdisjoint({"lgpio", "adafruit-lgpio", "rpi-gpio"})
    assert_native_requirements(
        parsed,
        {
            "sys_platform": "linux",
            "platform_machine": "aarch64",
            "python_version": f"3.{python_minor}",
        },
        True,
    )
    assert metadata["python_requires"] == ">=3.9.0"


@pytest.mark.parametrize(
    "compatible, expected",
    [
        (None, set()),
        (b"vendor,unknown-board", set()),
        (b"nvidia,tegra234", {"Jetson.GPIO"}),
        (b"ti,am335x", {"Adafruit_BBIO"}),
    ],
)
def test_other_setup_dependencies_are_unchanged(monkeypatch, compatible, expected):
    """Board-specific routing is unchanged; native markers ship on every host."""
    baseline = set(setup_metadata(monkeypatch, None)["install_requires"])
    requirements = set(setup_metadata(monkeypatch, compatible)["install_requires"])
    assert requirements == baseline | expected
    assert requirements.isdisjoint(PI_REQUIREMENTS)


def parse_requirements(values):
    """Normalize requirement names while retaining PEP 508 specifiers/markers."""
    return {
        canonicalize_name(requirement.name): requirement
        for value in values
        if value.strip() and not value.lstrip().startswith("#")
        for requirement in [Requirement(value)]
    }


def requirements_file():
    """Parse the static install list using PEP 508 marker semantics."""
    values = (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
    return parse_requirements(values)


def assert_native_requirements(requirements, environment, expected):
    """Check matching native dependency bounds and target-platform selection."""
    for name, specifier in NATIVE_SPECIFIERS.items():
        requirement = requirements[name]
        assert str(requirement.specifier) == specifier
        assert requirement.marker is not None
        assert requirement.marker.evaluate(environment) is expected


@pytest.mark.parametrize("python_version", ["3.9", "3.12", "3.13"])
@pytest.mark.parametrize("system, machine, expected", ARM_MARKER_CASES)
def test_static_pi_requirement_markers(system, machine, expected, python_version):
    """GPIO/PWM requirements use Linux ARM markers independent of Python age."""
    requirements = requirements_file()
    environment = {
        "sys_platform": system,
        "platform_machine": machine,
        "python_version": python_version,
    }
    assert_native_requirements(requirements, environment, expected)


@pytest.mark.parametrize("python_minor", [9, 12, 13])
@pytest.mark.parametrize("system, machine, expected", ARM_MARKER_CASES)
def test_metadata_without_board_detection_has_portable_native_dependencies(
    monkeypatch, system, machine, expected, python_minor
):
    """Universal metadata selects Linux ARM, including non-Pi boards.

    Architecture markers are not board detection; they intentionally apply to
    other Linux ARM systems too without changing those boards' backend routing.
    """
    metadata = setup_metadata(monkeypatch, None, python_minor)
    requirements = parse_requirements(metadata["install_requires"])
    environment = {
        "sys_platform": system,
        "platform_machine": machine,
        "python_version": f"3.{python_minor}",
    }
    assert_native_requirements(requirements, environment, expected)


def test_static_requirements_keep_jetson_gpio_dependency():
    """Jetson's existing PWM wrapper still imports the RPi.GPIO namespace."""
    requirements = requirements_file()
    assert "rpi-gpio" in requirements
    assert "lgpio" not in requirements
    assert "adafruit-lgpio" not in requirements


def load_importing(monkeypatch):
    """Load diagnostic helpers with no real board detection or GPIO imports."""
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.detector = SimpleNamespace()
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    spec = importlib.util.spec_from_file_location(
        "_test_blinka_importing", ROOT / "src" / "adafruit_blinka" / "importing.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "module_name, install_command",
    [
        ("gpiod", "pip install 'gpiod>=2.2.2,<3'"),
        (
            "adafruit_blinka_raspberry_pi_pwm",
            "pip install 'Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.1'",
        ),
    ],
)
def test_new_missing_dependency_hints(monkeypatch, module_name, install_command):
    """The static helper reports an install command without installing anything."""
    importing = load_importing(monkeypatch)
    error = ModuleNotFoundError(name=module_name)
    with pytest.raises(RuntimeError) as raised:
        importing.raise_for_missing_platform_dependency(error)
    assert install_command in str(raised.value)
    assert raised.value.__cause__ is error


def test_unknown_missing_dependency_is_preserved(monkeypatch):
    """Unrelated missing imports retain their original exception identity."""
    importing = load_importing(monkeypatch)
    error = ModuleNotFoundError(name="unrelated_library")
    with pytest.raises(ModuleNotFoundError) as raised:
        importing.raise_for_missing_platform_dependency(error)
    assert raised.value is error
