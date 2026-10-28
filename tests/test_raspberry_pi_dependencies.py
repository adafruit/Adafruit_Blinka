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
import shlex
import sys
from collections import namedtuple
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

ROOT = Path(__file__).parents[1]
BOARD_REQUIREMENTS = {
    "gpiod",
    "adafruit-blinka-raspberry-pi-pwm",
    "lgpio",
    "adafruit-lgpio",
    "rpi-gpio",
    "jetson-gpio",
    "rpi-ws281x",
    "adafruit-blinka-raspberry-pi5-neopixel",
    "adafruit-bbio",
}
CORE_REQUIREMENTS = {
    "adafruit-platformdetect",
    "adafruit-pureio",
    "binho-host-adapter",
    "pyftdi",
    "packaging",
    "adafruit-circuitpython-typing",
}
PLATFORM_CASES = [
    ("linux", "armv6l"),
    ("linux", "armv7l"),
    ("linux", "aarch64"),
    ("linux", "x86_64"),
    ("darwin", "arm64"),
    ("win32", "AMD64"),
    ("darwin", "aarch64"),
    ("win32", "aarch64"),
]
GPIO_MODULES = {
    "gpiod",
    "lgpio",
    "RPi",
    "Jetson",
    "Adafruit_BBIO",
    "adafruit_blinka_raspberry_pi_pwm",
    "adafruit_platformdetect",
}
VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")


def setup_metadata(monkeypatch, python_minor=12):
    """Capture universal metadata, rejecting hardware detection and imports."""
    captured = {}
    setuptools = ModuleType("setuptools")
    setuptools.setup = lambda **kwargs: captured.update(kwargs)
    setuptools.find_packages = lambda _directory: ["adafruit_blinka", "micropython"]
    original_exists = os.path.exists
    original_open = builtins.open
    original_io_open = io.open
    original_import = builtins.__import__

    def exists(path):
        assert not os.fspath(path).startswith("/proc/")
        return original_exists(path)

    def open_without_hardware(path, *args, **kwargs):
        assert not os.fspath(path).startswith("/proc/")
        return original_open(path, *args, **kwargs)

    def io_open_without_hardware(path, *args, **kwargs):
        assert not os.fspath(path).startswith("/proc/")
        return original_io_open(path, *args, **kwargs)

    def import_without_gpio(name, *args, **kwargs):
        assert name.split(".")[0] not in GPIO_MODULES
        return original_import(name, *args, **kwargs)

    with monkeypatch.context() as patches:
        patches.setitem(sys.modules, "setuptools", setuptools)
        patches.setattr(os.path, "exists", exists)
        patches.setattr(builtins, "open", open_without_hardware)
        patches.setattr(io, "open", io_open_without_hardware)
        patches.setattr(builtins, "__import__", import_without_gpio)
        patches.setattr(
            sys, "version_info", VersionInfo(3, python_minor, 0, "final", 0)
        )
        runpy.run_path(str(ROOT / "setup.py"), run_name="__main__")
    return captured


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


def assert_minimal_requirements(requirements, environment):
    """Only portable base dependencies belong in installation metadata."""
    assert set(requirements).isdisjoint(BOARD_REQUIREMENTS)
    assert set(requirements) == CORE_REQUIREMENTS | {"sysv-ipc", "toml"}
    for name, specifier in (
        ("adafruit-platformdetect", ">=3.90.0"),
        ("packaging", ">=20.0"),
    ):
        requirement = requirements[name]
        assert str(requirement.specifier) == specifier
        assert requirement.marker is None

    active = {
        name
        for name, requirement in requirements.items()
        if requirement.marker is None or requirement.marker.evaluate(environment)
    }
    expected = set(CORE_REQUIREMENTS)
    if environment["sys_platform"] == "linux":
        expected.add("sysv-ipc")
    if environment["python_version"] == "3.9":
        expected.add("toml")
    assert active == expected


@pytest.mark.parametrize("python_version", ["3.9", "3.12", "3.13"])
@pytest.mark.parametrize("system, machine", PLATFORM_CASES)
def test_static_requirements_are_minimal(system, machine, python_version):
    """Static requirements do not install hardware backends on any platform."""
    requirements = requirements_file()
    environment = {
        "sys_platform": system,
        "platform_machine": machine,
        "python_version": python_version,
    }
    assert_minimal_requirements(requirements, environment)


@pytest.mark.parametrize("python_minor", [9, 12, 13])
@pytest.mark.parametrize("system, machine", PLATFORM_CASES)
def test_metadata_is_minimal_without_hardware_detection(
    monkeypatch, system, machine, python_minor
):
    """Build hosts produce identical minimal metadata for all target systems."""
    metadata = setup_metadata(monkeypatch, python_minor)
    requirements = parse_requirements(metadata["install_requires"])
    environment = {
        "sys_platform": system,
        "platform_machine": machine,
        "python_version": f"3.{python_minor}",
    }
    assert_minimal_requirements(requirements, environment)
    assert metadata["python_requires"] == ">=3.9.0"


def test_metadata_preserves_micropython_package(monkeypatch):
    """Keep the shared MicroPython package instead of restoring its old module."""
    metadata = setup_metadata(monkeypatch)
    assert metadata["packages"] == ["adafruit_blinka", "micropython"]
    assert "micropython" not in metadata["py_modules"]
    assert "micropython-stubs" not in metadata["packages"]
    assert metadata["package_data"]["micropython"] == ["py.typed"]


def load_importing(monkeypatch, detector=None):
    """Load diagnostic helpers with no real board detection or GPIO imports."""
    agnostic = ModuleType("adafruit_blinka.agnostic")
    if detector is None:
        detector = SimpleNamespace(
            board=SimpleNamespace(
                id="RASPBERRY_PI_4B",
                any_raspberry_pi=True,
                any_raspberry_pi_5_board=False,
                any_jetson_board=False,
            ),
            chip=SimpleNamespace(id="BCM2711"),
        )
    agnostic.detector = detector
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    spec = importlib.util.spec_from_file_location(
        "_test_blinka_importing", ROOT / "src" / "adafruit_blinka" / "importing.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "module_name, requirement",
    [
        ("gpiod", "gpiod>=2.2.2,<3"),
        (
            "adafruit_blinka_raspberry_pi_pwm",
            "Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2",
        ),
    ],
)
def test_new_missing_dependency_hints(monkeypatch, module_name, requirement):
    """The helper targets the running interpreter without installing anything."""
    importing = load_importing(monkeypatch)
    error = ModuleNotFoundError(name=module_name)
    with pytest.raises(RuntimeError) as raised:
        importing.raise_for_missing_platform_dependency(error)
    install_command = shlex.join([sys.executable, "-m", "pip", "install", requirement])
    assert install_command in str(raised.value)
    assert raised.value.__cause__ is error


def test_unknown_missing_dependency_is_preserved(monkeypatch):
    """Unrelated missing imports retain their original exception identity."""
    importing = load_importing(monkeypatch)
    error = ModuleNotFoundError(name="unrelated_library")
    with pytest.raises(ModuleNotFoundError) as raised:
        importing.raise_for_missing_platform_dependency(error)
    assert raised.value is error


@pytest.mark.parametrize(
    "chip_id, is_jetson, module_name, requirement",
    [
        ("GENERIC_X86", False, "gpiod", "gpiod"),
        ("TEGRA210", True, "RPi", "Jetson.GPIO"),
    ],
)
def test_non_pi_missing_dependency_hints(
    monkeypatch, chip_id, is_jetson, module_name, requirement
):
    """Generic gpiod stays unbounded and Jetson uses its own RPi provider."""
    detector = SimpleNamespace(
        board=SimpleNamespace(
            id="JETSON_NANO" if is_jetson else "GENERIC_LINUX_PC",
            any_raspberry_pi=False,
            any_raspberry_pi_5_board=False,
            any_jetson_board=is_jetson,
        ),
        chip=SimpleNamespace(id=chip_id),
    )
    importing = load_importing(monkeypatch, detector)
    error = ModuleNotFoundError(name=module_name)
    with pytest.raises(RuntimeError) as raised:
        importing.raise_for_missing_platform_dependency(error)
    install_command = shlex.join([sys.executable, "-m", "pip", "install", requirement])
    assert install_command in str(raised.value)
    assert raised.value.__cause__ is error
