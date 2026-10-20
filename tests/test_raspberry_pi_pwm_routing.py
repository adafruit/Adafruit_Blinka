# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Test public pwmio routing without importing GPIO libraries or hardware."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

PREFIX = "adafruit_blinka.microcontroller."


class BoardFlags(SimpleNamespace):
    """Return false for board families not selected by the test."""

    def __getattr__(self, _name):
        return False


@pytest.mark.parametrize(
    "flags, selected",
    [
        ({"any_raspberry_pi": True}, "generic_linux.raspberry_pi_pwmout"),
        ({"any_raspberry_pi_5_board": True}, "generic_linux.raspberry_pi_pwmout"),
        (
            {"any_raspberry_pi": True, "any_raspberry_pi_5_board": True},
            "generic_linux.raspberry_pi_pwmout",
        ),
        ({"any_bananapi": True}, "generic_linux.sysfs_pwmout"),
        ({"any_jetson_board": True}, "tegra.PWMOut"),
    ],
)
def test_public_pwmio_routing(monkeypatch, flags, selected):
    """Both Pi families switch, while unrelated backend selection is unchanged."""
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.detector = SimpleNamespace(board=BoardFlags(**flags))
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    importing = ModuleType("adafruit_blinka.importing")
    checks = []
    importing.check_platform_dependency = checks.append
    importing.raise_for_missing_platform_dependency = pytest.fail
    monkeypatch.setitem(sys.modules, "adafruit_blinka.importing", importing)
    backends = {}
    for name in (
        "generic_linux.raspberry_pi_pwmout",
        "generic_linux.rpi_gpio_pwmout",
        "generic_linux.lgpio_pwmout",
        "generic_linux.sysfs_pwmout",
        "tegra.PWMOut",
    ):
        module_name = PREFIX + name
        module = ModuleType(module_name)
        module.PWMOut = object()
        backends[name] = module.PWMOut
        monkeypatch.setitem(sys.modules, module_name, module)
    spec = importlib.util.spec_from_file_location(
        "_test_public_pwmio", Path(__file__).parents[1] / "src" / "pwmio.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.PWMOut is backends[selected]
    assert checks == (
        ["adafruit_blinka_raspberry_pi_pwm"]
        if selected == "generic_linux.raspberry_pi_pwmout"
        else []
    )
