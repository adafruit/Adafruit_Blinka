# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Validate optional backends only when their public feature is imported."""

# Pytest provides the named monkeypatch fixture.
# pylint: disable=redefined-outer-name

import builtins
import importlib.util
import shlex
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

from adafruit_blinka import platform_dependencies

ROOT = Path(__file__).parents[1] / "src"
PREFIX = "adafruit_blinka.microcontroller."


class BoardFlags(SimpleNamespace):
    """Default unused board-family selectors to false."""

    def __getattr__(self, _name):
        return False


def load_module(name, path):
    """Execute a public module under a private, uncached name."""
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_feature_import(monkeypatch, **flags):
    """Select hardware without loading its detector, pins, or native code."""
    detector = SimpleNamespace(
        board=BoardFlags(**flags), chip=SimpleNamespace(id="BCM2711")
    )
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.detector = detector
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    importing = load_module("_test_feature_importing", "adafruit_blinka/importing.py")
    monkeypatch.setitem(sys.modules, "adafruit_blinka.importing", importing)
    monkeypatch.setitem(
        sys.modules, "adafruit_blinka.platform_dependencies", platform_dependencies
    )
    monkeypatch.setattr(
        platform_dependencies.subprocess,
        "run",
        lambda *_args, **_kwargs: pytest.fail("Feature imports must never run pip"),
    )
    return importing, detector


def test_cpython_feature_check_uses_selected_detector(monkeypatch):
    """The import helper delegates to the non-installing platform check."""
    importing, detector = prepare_feature_import(monkeypatch, any_raspberry_pi=True)
    calls = []
    monkeypatch.setattr(
        platform_dependencies,
        "check_platform_dependency",
        lambda *args: calls.append(args),
    )

    importing.check_platform_dependency("adafruit_blinka_raspberry_pi_pwm")

    assert calls == [(detector, "adafruit_blinka_raspberry_pi_pwm")]


@pytest.mark.parametrize("implementation", ["micropython", "circuitpython"])
def test_embedded_feature_check_does_not_import_cpython_helper(
    monkeypatch, implementation
):
    """Embedded interpreters must not load packaging or importlib.metadata."""
    importing, _detector = prepare_feature_import(monkeypatch)
    real_import = builtins.__import__

    def no_platform_helper(name, *args, **kwargs):
        assert name != "adafruit_blinka.platform_dependencies"
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", no_platform_helper)
    monkeypatch.setattr(sys, "implementation", SimpleNamespace(name=implementation))

    importing.check_platform_dependency("adafruit_blinka_raspberry_pi_pwm")


@pytest.mark.parametrize(
    "flags, backend, dependency",
    [
        (
            {"any_raspberry_pi": True},
            PREFIX + "bcm283x.neopixel",
            "_rpi_ws281x",
        ),
        (
            {"any_raspberry_pi": True, "any_raspberry_pi_5_board": True},
            "adafruit_raspberry_pi5_neopixel_write",
            "adafruit_raspberry_pi5_neopixel_write",
        ),
        ({"pico_u2if": True}, PREFIX + "rp2040_u2if.neopixel", None),
        (
            {"OS_AGNOSTIC_BOARD": True},
            PREFIX + "generic_agnostic_board.neopixel",
            None,
        ),
    ],
)
def test_neopixel_checks_only_selected_pi_backend(
    monkeypatch, flags, backend, dependency
):
    """NeoPixels never validate PWM or change non-Pi feature selection."""
    importing, _detector = prepare_feature_import(monkeypatch, **flags)
    checks = []
    monkeypatch.setattr(importing, "check_platform_dependency", checks.append)
    native = ModuleType(backend)
    native.neopixel_write = lambda gpio, buf: (gpio, buf)
    monkeypatch.setitem(sys.modules, backend, native)

    neopixel = load_module("_test_feature_neopixel", "neopixel_write.py")

    assert checks == ([dependency] if dependency is not None else [])
    assert neopixel.neopixel_write("pin", b"rgb") == ("pin", b"rgb")


@pytest.mark.parametrize(
    "feature, distribution, flags, expected",
    [
        (
            "pwmio.py",
            "Adafruit-Blinka-Raspberry-Pi-PWM",
            {"any_raspberry_pi": True},
            "Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2",
        ),
        (
            "neopixel_write.py",
            "rpi_ws281x",
            {"any_raspberry_pi": True},
            "rpi_ws281x>=4.0.0",
        ),
    ],
)
def test_incompatible_optional_backend_fails_only_at_feature_import(
    monkeypatch, feature, distribution, flags, expected
):
    """The selected feature rejects its installed old backend without pip."""
    _importing, _detector = prepare_feature_import(monkeypatch, **flags)
    inspected = []

    def installed_version(name):
        inspected.append(name)
        assert name == distribution
        return "0.0.1"

    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", installed_version
    )
    assert not inspected

    with pytest.raises(RuntimeError) as raised:
        load_module("_test_incompatible_feature", feature)

    assert expected in str(raised.value)
    assert inspected


@pytest.mark.parametrize(
    "version, supported",
    [
        ("1.0.0", False),
        ("1.0.1", False),
        ("1.0.2rc1", False),
        ("1.0.2", True),
        ("1.1.0", True),
    ],
)
def test_pwm_minimum_requires_system_gpiod_compatible_release(
    monkeypatch, version, supported
):
    """Older PWM metadata must not replace maintained system gpiod transitively."""
    _importing, detector = prepare_feature_import(monkeypatch, any_raspberry_pi=True)
    module = "adafruit_blinka_raspberry_pi_pwm"
    requirement = platform_dependencies.get_platform_requirement_for_import(
        detector, module
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.util, "find_spec", lambda _name: object()
    )
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", lambda _name: version
    )
    assert (
        platform_dependencies._requirement_available(  # pylint: disable=protected-access
            module, requirement
        )
        is supported
    )
    if supported:
        platform_dependencies.check_platform_dependency(detector, module)
    else:
        with pytest.raises(RuntimeError, match="PWM>=1.0.2"):
            platform_dependencies.check_platform_dependency(detector, module)


def test_pi5_neopixel_reports_unsupported_python_before_native_import(monkeypatch):
    """An installed backend cannot hide the Pi 5 package's Python floor."""
    _importing, _detector = prepare_feature_import(
        monkeypatch, any_raspberry_pi=True, any_raspberry_pi_5_board=True
    )
    monkeypatch.setattr(sys, "version_info", (3, 10, 0, "final", 0))
    native = ModuleType("adafruit_raspberry_pi5_neopixel_write")
    monkeypatch.setitem(sys.modules, "adafruit_raspberry_pi5_neopixel_write", native)

    with pytest.raises(RuntimeError, match="Python 3.11 or newer"):
        load_module("_test_unsupported_neopixel", "neopixel_write.py")


@pytest.mark.parametrize(
    "feature, module_name, import_statement, requirement, flags",
    [
        (
            "pwmio.py",
            "adafruit_blinka_raspberry_pi_pwm",
            PREFIX + "generic_linux.raspberry_pi_pwmout",
            "Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2",
            {"any_raspberry_pi": True},
        ),
        (
            "neopixel_write.py",
            "_rpi_ws281x",
            PREFIX + "bcm283x",
            "rpi_ws281x>=4.0.0",
            {"any_raspberry_pi": True},
        ),
        (
            "neopixel_write.py",
            "adafruit_raspberry_pi5_neopixel_write",
            "adafruit_raspberry_pi5_neopixel_write",
            "Adafruit-Blinka-Raspberry-Pi5-Neopixel",
            {"any_raspberry_pi": True, "any_raspberry_pi_5_board": True},
        ),
    ],
)
def test_missing_optional_backend_retains_recovery_command(
    monkeypatch, feature, module_name, import_statement, requirement, flags
):  # pylint: disable=too-many-arguments
    """Missing modules retain current-interpreter guidance, not a pip attempt."""
    importing, _detector = prepare_feature_import(monkeypatch, **flags)
    monkeypatch.setattr(importing, "check_platform_dependency", lambda _name: None)
    if module_name == "adafruit_raspberry_pi5_neopixel_write":
        # Exercise missing-package guidance on a supported target Python,
        # independently of the interpreter used to run this test.
        monkeypatch.setattr(sys, "version_info", (3, 11, 0, "final", 0))
    real_import = builtins.__import__
    missing = ModuleNotFoundError(name=module_name)

    def import_without_backend(name, *args, **kwargs):
        if name == import_statement:
            raise missing
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", import_without_backend)

    with pytest.raises(RuntimeError) as raised:
        load_module("_test_missing_feature", feature)

    command = shlex.join([sys.executable, "-m", "pip", "install", requirement])
    assert command in str(raised.value)
    assert raised.value.__cause__ is missing
