# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Discovered PWM chip numbers survive board definitions and sysfs path selection."""

import importlib.util
import sys
from os.path import join
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

import adafruit_blinka

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name

SOURCE = Path(__file__).parents[1] / "src/adafruit_blinka/microcontroller"
CASES = [
    (
        "amlogic/meson_g12_common",
        "ODROID_C4",
        {
            "ffd1b000.pwm": [(0, "GPIOX_6", "PWMA"), (1, "GPIOX_19", "PWMB")],
            "ffd1a000.pwm": [(0, "GPIOX_5", "PWMC"), (1, "GPIOX_3", "PWMD")],
            "ffd19000.pwm": [(0, "GPIOX_16", "PWME"), (1, "GPIOX_7", "PWMF")],
        },
    ),
    (
        "amlogic/meson_g12_common",
        "ODROID_N2",
        {
            "ffd1a000.pwm": [(0, "GPIOX_5", "PWMC"), (1, "GPIOX_6", "PWMD")],
            "ffd19000.pwm": [(0, "GPIOX_16", "PWME"), (1, "GPIOX_7", "PWMF")],
        },
    ),
    (
        "rockchip/rk3566",
        "ODROID_M1S",
        {
            "fdd70010.pwm": [(0, "GPIO0_B5", None)],
            "fdd70020.pwm": [(0, "GPIO0_B6", None)],
            "fdd70030.pwm": [(0, "GPIO0_C2", None)],
        },
    ),
    (
        "rockchip/rk3566",
        "RADXA_ZERO3",
        {
            "fe6f0000.pwm": [(0, "GPIO3_B1", None)],
            "fe6f0010.pwm": [(0, "GPIO3_B2", None)],
        },
    ),
    (
        "rockchip/rk3568b2",
        "ODROID_M1",
        {
            "fdd70010.pwm": [(0, "GPIO0B_5", None)],
            "fdd70020.pwm": [(0, "GPIO0B_6", None)],
            "fe6f0010.pwm": [(0, "GPIO3B_2", None)],
        },
    ),
    (
        "spacemit/k1",
        "BANANA_PI_F3",
        {
            "d401bc00.pwm": [(0, "GPIO_92", None)],
            "d4020400.pwm": [(0, "GPIO_74", None)],
        },
    ),
]


def load_source(monkeypatch, name, path):
    """Load production source without real board or GPIO imports."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, module)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def board_loader(monkeypatch):
    """Use real alias discovery with fake sysfs paths and inert Pin/Chip types."""

    class Pin:  # pylint: disable=too-few-public-methods
        """Record pin identities without touching a GPIO controller."""

        def __init__(self, pin_id):
            self.id = pin_id

    class Chip:  # pylint: disable=too-few-public-methods
        """Provide only the line counts queried by the Amlogic definitions."""

        def __init__(self, chip_id):
            self.num_lines = 10 if chip_id == "0" else 85

    pin_module_name = "adafruit_blinka.microcontroller.generic_linux.libgpiod_pin"
    chip_module_name = "adafruit_blinka.microcontroller.generic_linux.libgpiod_chip"
    pin_module = ModuleType(pin_module_name)
    pin_module.Pin = Pin
    chip_module = ModuleType(chip_module_name)
    chip_module.Chip = Chip
    monkeypatch.setitem(sys.modules, pin_module_name, pin_module)
    monkeypatch.setitem(sys.modules, chip_module_name, chip_module)
    aliases = load_source(
        monkeypatch, "adafruit_blinka.microcontroller.alias", SOURCE / "alias.py"
    )

    def load(module_path, board_id, devices):
        agnostic = ModuleType("adafruit_blinka.agnostic")
        agnostic.detector = SimpleNamespace(board=SimpleNamespace(id=board_id))
        monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
        monkeypatch.setattr(adafruit_blinka, "agnostic", agnostic, raising=False)
        paths = {
            f"/sys/class/pwm/pwmchip{chip}": f"/sys/devices/platform/{device}/pwm/pwmchip{chip}"
            for device, chip in devices.items()
        }
        aliases.os = SimpleNamespace(
            path=SimpleNamespace(exists=paths.__contains__, realpath=paths.__getitem__)
        )
        return load_source(
            monkeypatch, "_test_pwm_board", SOURCE / module_path / "pin.py"
        )

    return load


def baseline_entries(module, module_path):
    """Keep RK3566's existing static definitions outside this discovery fix."""
    if module_path == "rockchip/rk3566":
        return [((0, 0), module.PWM0), ((0, 0), module.PWM1)]
    return []


def check_mapping(module, module_path, devices, mappings):
    """Check exact channels, pin identities, existing names, and container types."""
    expected = []
    for device, pin_mappings in mappings.items():
        if device not in devices:
            continue
        chip = devices[device]
        for channel, pin_name, alias_name in pin_mappings:
            pin = getattr(module, pin_name)
            expected.append(((chip, channel), pin))
            # Preserve existing dynamic alias names, even their doubled PWM prefix.
            assert getattr(module, alias_name or f"PWMPWM{chip}") is pin
    assert list(module.pwmOuts) == baseline_entries(module, module_path) + expected
    expected_type = list if module_path == "spacemit/k1" else tuple
    assert isinstance(module.pwmOuts, expected_type)
    return expected


def check_sysfs_paths(monkeypatch, board_module, entries):
    """Stop real PWMOut before file access, after it selects its controller path."""
    controller = ModuleType("microcontroller")
    controller.__path__ = []
    controller.pin = board_module
    monkeypatch.setitem(sys.modules, "microcontroller", controller)
    monkeypatch.setitem(sys.modules, "microcontroller.pin", board_module)
    backend = load_source(
        monkeypatch, "_test_alias_sysfs_pwm", SOURCE / "generic_linux/sysfs_pwmout.py"
    )
    paths = []

    def missing_directory(path):
        paths.append(path)
        return False

    def forbidden_open(*_args, **_kwargs):
        pytest.fail("sysfs selection checks must not open device files")

    backend.os = SimpleNamespace(
        path=SimpleNamespace(join=join, isdir=missing_directory)
    )
    backend.open = forbidden_open
    monkeypatch.setattr(backend.PWMOut, "deinit", lambda _self: None)
    for (chip, _channel), pin in entries:
        with pytest.raises(ValueError, match="PWM channel does not exist"):
            backend.PWMOut(pin)
        assert paths[-1] == f"/sys/class/pwm/pwmchip{chip}"
    assert len(paths) == len(entries)


@pytest.mark.parametrize("case", CASES, ids=[c[1] for c in CASES])
@pytest.mark.parametrize("first_chip", [0, 9, 10, 29])
def test_discovered_chip_numbers_reach_pwmout(
    board_loader, monkeypatch, case, first_chip
):
    module_path, board_id, mappings = case
    devices = {device: first_chip + index for index, device in enumerate(mappings)}
    module = board_loader(module_path, board_id, devices)
    entries = check_mapping(module, module_path, devices, mappings)
    check_sysfs_paths(monkeypatch, module, entries)


@pytest.mark.parametrize("case", CASES, ids=[c[1] for c in CASES])
@pytest.mark.parametrize("presence", ["none", "first", "last"])
def test_missing_or_partial_discovery_preserves_other_definitions(
    board_loader, monkeypatch, case, presence
):
    module_path, board_id, mappings = case
    names = list(mappings)
    if presence == "none":
        devices = {}
    else:
        devices = {names[0 if presence == "first" else -1]: 31}
    module = board_loader(module_path, board_id, devices)
    entries = check_mapping(module, module_path, devices, mappings)
    check_sysfs_paths(monkeypatch, module, entries)


@pytest.mark.parametrize("module_path", sorted({c[0] for c in CASES}))
def test_unrelated_board_keeps_static_definitions(board_loader, module_path):
    module = board_loader(module_path, "UNRELATED_BOARD", {})
    assert list(module.pwmOuts) == baseline_entries(module, module_path)
