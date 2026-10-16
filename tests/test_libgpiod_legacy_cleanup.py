# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Exercise both supported libgpiod 1.x chip cleanup APIs without GPIO access."""

import importlib.util
from pathlib import Path
import sys
import types

import pytest

# Tests inspect resource ownership and explicitly repeat destructors. Binding
# fakes preserve the instance-method APIs even where they do not use self.
# pylint: disable=protected-access,redefined-outer-name,unnecessary-dunder-call,no-self-use,too-few-public-methods

DRIVER_DIRECTORY = (
    Path(__file__).resolve().parents[1]
    / "src/adafruit_blinka/microcontroller/generic_linux/libgpiod"
)


def load_driver(name, monkeypatch, binding):
    """Load a driver against a fake binding without importing board detection."""
    monkeypatch.setitem(sys.modules, "gpiod", binding)
    spec = importlib.util.spec_from_file_location(name, DRIVER_DIRECTORY / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(params=("official", "legacy"))
def drivers(request, monkeypatch):
    """Mirror official Chip.close()/num_lines() and legacy chip.reset()/property."""
    events = []

    class Line:
        def __init__(self):
            self.fail_release = False

        def release(self):
            events.append("release")
            if self.fail_release:
                self.fail_release = False
                raise OSError("line release failed")

    class OfficialLine(Line):
        def request(
            self, *, consumer, type, flags, default_vals
        ):  # pylint: disable=redefined-builtin
            assert consumer == "adafruit_blinka"
            assert type == 3
            assert flags == 0
            assert default_vals == [0]

    class LegacyLine(Line):
        def request(self, config, default_val=0):
            assert config.consumer == "adafruit_blinka"
            assert config.request_type == 3
            assert default_val == 0

    class ChipBase:
        OPEN_BY_NUMBER = 5
        OPEN_BY_NAME = 3
        fail_open = False

        def __init__(self, _device, _how=None):
            if self.fail_open:
                raise OSError("chip open failed")
            self.fail_cleanup = False
            self.line = OfficialLine() if request.param == "official" else LegacyLine()

        def get_line(self, offset):
            assert offset == 18
            return self.line

        def cleanup(self, operation):
            events.append(operation)
            if self.fail_cleanup:
                self.fail_cleanup = False
                raise OSError("chip cleanup failed")

    class OfficialChip(ChipBase):
        def num_lines(self):
            return 32

        def close(self):
            self.cleanup("close")

    class LegacyChip(ChipBase):
        @property
        def num_lines(self):
            return 32

        def reset(self):
            self.cleanup("reset")

    class LineRequest:
        DIRECTION_INPUT = 1
        DIRECTION_OUTPUT = 3

        def __init__(self):
            self.consumer = ""
            self.request_type = 0

    binding = types.ModuleType("gpiod")
    if request.param == "official":
        binding.Chip = OfficialChip
        binding.LINE_REQ_DIR_IN = 1
        binding.LINE_REQ_DIR_OUT = 3
        chip_type = OfficialChip
        cleanup = "close"
    else:
        binding.chip = LegacyChip
        binding.line_request = LineRequest
        chip_type = LegacyChip
        cleanup = "reset"

    pin_driver = load_driver("libgpiod_pin_1_x", monkeypatch, binding)
    chip_driver = load_driver("libgpiod_chip_1_x", monkeypatch, binding)
    return types.SimpleNamespace(
        Pin=pin_driver.Pin,
        Chip=chip_driver.Chip,
        chip_type=chip_type,
        cleanup=cleanup,
        events=events,
    )


def test_pin_releases_line_before_chip_once(drivers):
    pin = drivers.Pin(18)
    pin.init(mode=pin.OUT)
    drivers.events.clear()

    pin.deinit()
    pin.deinit()
    pin.__del__()

    assert drivers.events == ["release", drivers.cleanup]
    assert pin._line is None
    assert pin._chip is None


def test_pin_cleanup_without_line_request(drivers):
    pin = drivers.Pin((0, 18))
    assert drivers.events == []
    pin._ensure_chip()
    pin.deinit()
    pin.deinit()

    assert drivers.events == [drivers.cleanup]


def test_chip_constructor_and_repeated_cleanup(drivers):
    chip = drivers.Chip("gpiochip0")
    assert chip.num_lines == 32

    chip.__del__()
    chip.__del__()

    assert drivers.events == [drivers.cleanup]
    assert chip._chip is None


@pytest.mark.parametrize("driver_name", ("Pin", "Chip"))
def test_failed_open_can_be_cleaned_up(drivers, driver_name):
    driver = getattr(drivers, driver_name)
    instance = driver.__new__(driver)
    drivers.chip_type.fail_open = True
    identifier = 18 if driver_name == "Pin" else "gpiochip0"

    with pytest.raises(OSError, match="chip open failed"):
        instance.__init__(identifier)
        if driver_name == "Pin":
            instance.init()
    instance.__del__()

    assert drivers.events == []


def test_pin_retains_chip_after_cleanup_failure(drivers):
    pin = drivers.Pin(18)
    pin.init(mode=pin.OUT)
    chip = pin._chip
    chip.fail_cleanup = True
    drivers.events.clear()

    with pytest.raises(OSError, match="chip cleanup failed"):
        pin.deinit()
    assert pin._line is None
    assert pin._chip is chip
    pin.deinit()

    assert drivers.events == ["release", drivers.cleanup, drivers.cleanup]
    assert pin._chip is None


def test_chip_retains_owner_after_cleanup_failure(drivers):
    chip = drivers.Chip("gpiochip0")
    owner = chip._chip
    owner.fail_cleanup = True

    with pytest.raises(OSError, match="chip cleanup failed"):
        chip.__del__()
    assert chip._chip is owner
    chip.__del__()

    assert drivers.events == [drivers.cleanup, drivers.cleanup]
    assert chip._chip is None


def test_pin_retains_line_and_chip_after_release_failure(drivers):
    pin = drivers.Pin(18)
    pin.init(mode=pin.OUT)
    line = pin._line
    chip = pin._chip
    line.fail_release = True
    drivers.events.clear()

    with pytest.raises(OSError, match="line release failed"):
        pin.deinit()
    assert pin._line is line
    assert pin._chip is chip
    pin.deinit()

    assert drivers.events == ["release", "release", drivers.cleanup]
    assert pin._line is None
    assert pin._chip is None
