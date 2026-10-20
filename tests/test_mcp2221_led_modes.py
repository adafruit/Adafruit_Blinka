# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""MCP2221 activity indicators, tested without board imports or physical HID."""

import atexit
import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from unittest.mock import Mock, call

import pytest

# Pytest supplies the named fixtures; state assertions cover the mode cache.
# pylint: disable=redefined-outer-name,protected-access

SOURCE = Path(__file__).parents[1] / "src/adafruit_blinka/microcontroller/mcp2221"
LED_CASES = [
    (0, "LED_URX", "GP_ALT0"),
    (1, "LED_UTX", "GP_ALT1"),
    (3, "LED_I2C", "GP_DEDICATED"),
]


def load_source(name, filename):
    """Execute production source under a test-only module name."""
    spec = importlib.util.spec_from_file_location(name, SOURCE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def pin_backend(monkeypatch):
    """Provide an inert relative backend so importing Pin cannot open HID."""
    name = "_test_mcp2221_leds"
    package = ModuleType(name)
    package.__path__ = [str(SOURCE)]
    backend = Mock(GP_GPIO=0, GP_DEDICATED=1, GP_ALT0=2, GP_ALT1=3)
    backend_name = name + ".mcp2221"
    backend_module = ModuleType(backend_name)
    backend_module.mcp2221 = backend
    monkeypatch.setitem(sys.modules, name, package)
    monkeypatch.setitem(sys.modules, backend_name, backend_module)
    return load_source(name + ".pin", "pin.py"), backend


@pytest.mark.parametrize("pin_id,mode_name,raw_name", LED_CASES)
def test_led_mode_mapping(pin_backend, pin_id, mode_name, raw_name):
    module, backend = pin_backend
    pin = module.Pin(pin_id)
    mode = getattr(module.Pin, mode_name)
    pin.init(mode)
    assert pin._mode == mode
    assert backend.mock_calls == [call.gp_set_mode(pin_id, getattr(backend, raw_name))]


@pytest.mark.parametrize(
    "pin_id,mode_name",
    [
        (pin_id, mode_name)
        for valid_pin, mode_name, _ in LED_CASES
        for pin_id in range(4)
        if pin_id != valid_pin
    ],
)
def test_wrong_led_pin_is_rejected_before_io(pin_backend, pin_id, mode_name):
    module, backend = pin_backend
    pin = module.Pin(pin_id)
    pin.init(module.Pin.OUT)
    backend.reset_mock()
    with pytest.raises(ValueError):
        pin.init(getattr(module.Pin, mode_name))
    assert pin._mode == module.Pin.OUT
    assert backend.mock_calls == []


@pytest.mark.parametrize("pin_id,mode_name,_raw_name", LED_CASES)
def test_led_modes_reject_pull_and_none_id(pin_backend, pin_id, mode_name, _raw_name):
    module, backend = pin_backend
    mode = getattr(module.Pin, mode_name)
    pin = module.Pin(pin_id)
    with pytest.raises(NotImplementedError):
        pin.init(mode, pull=True)
    assert pin._mode is None
    pin = module.Pin()
    with pytest.raises(RuntimeError):
        pin.init(mode)
    assert pin._mode is None
    assert backend.mock_calls == []


@pytest.mark.parametrize("pin_id,mode_name,raw_name", LED_CASES)
def test_led_backend_failure_preserves_mode(pin_backend, pin_id, mode_name, raw_name):
    module, backend = pin_backend
    pin = module.Pin(pin_id)
    pin.init(module.Pin.OUT)
    backend.reset_mock()
    backend.gp_set_mode.side_effect = OSError("HID failed")
    with pytest.raises(OSError, match="HID failed"):
        pin.init(getattr(module.Pin, mode_name))
    assert pin._mode == module.Pin.OUT
    assert backend.mock_calls == [call.gp_set_mode(pin_id, getattr(backend, raw_name))]


@pytest.mark.parametrize("pin_id,mode_name,_raw_name", LED_CASES)
def test_led_value_has_no_io(pin_backend, pin_id, mode_name, _raw_name):
    module, backend = pin_backend
    pin = module.Pin(pin_id)
    pin.init(getattr(module.Pin, mode_name))
    backend.reset_mock()
    for value in (None, module.Pin.LOW, module.Pin.HIGH):
        with pytest.raises(RuntimeError):
            pin.value(value)
    assert backend.mock_calls == []


@pytest.mark.parametrize("pin_id,mode_name,_raw_name", LED_CASES)
@pytest.mark.parametrize("direction", [0, 1])
def test_led_can_return_to_gpio(pin_backend, pin_id, mode_name, _raw_name, direction):
    module, backend = pin_backend
    pin = module.Pin(pin_id)
    pin.init(getattr(module.Pin, mode_name))
    backend.reset_mock()
    pin.init(direction)
    assert pin._mode == direction
    assert backend.mock_calls == [
        call.gp_set_mode(pin_id, backend.GP_GPIO),
        call.gpio_set_direction(pin_id, direction),
    ]


def test_existing_gpio_and_analog_modes(pin_backend):
    module, backend = pin_backend
    assert (
        module.Pin.OUT,
        module.Pin.IN,
        module.Pin.ADC,
        module.Pin.DAC,
    ) == (0, 1, 2, 3)
    pin = module.Pin(0)
    pin.init()
    assert pin._mode == module.Pin.IN
    assert backend.mock_calls == [call.gp_set_mode(0, 0), call.gpio_set_direction(0, 1)]

    backend.reset_mock()
    pin = module.Pin(1)
    pin.init(module.Pin.ADC)
    backend.adc_read.return_value = 1023
    assert pin.value() == 65472
    assert backend.mock_calls == [
        call.gp_set_mode(1, 2),
        call.adc_configure(),
        call.adc_read(1),
    ]

    backend.reset_mock()
    pin = module.Pin(2)
    pin.init(module.Pin.DAC)
    pin.value(65535)
    assert backend.mock_calls == [
        call.gp_set_mode(2, 3),
        call.dac_configure(),
        call.dac_write(2, 31),
    ]


class InertHID:
    """Accept and record real driver reports without opening any USB device."""

    def __init__(self):
        self.commands = []
        self.opened = False

    def open(self, vendor_id, product_id):
        """Validate device selection without accessing hardware."""
        assert (vendor_id, product_id) == (0x04D8, 0x00DD)
        self.opened = True

    def close(self):
        """Release the inert transport."""
        self.opened = False

    def write(self, report):
        """Record one complete HID report without its report ID."""
        assert self.opened
        assert len(report) == 65
        assert report[0] == 0
        self.commands.append(bytes(report[1:]))
        return len(report)

    def read(self, length):
        """Return a successful response with the command echo."""
        assert self.opened
        assert length == 64
        response = bytearray(length)
        response[0] = self.commands[-1][0]
        return response


@pytest.fixture
def real_backend(monkeypatch):
    """Import the production backend with inert HID and reset disabled."""
    device = InertHID()
    hid = ModuleType("hid")
    hid.device = lambda: device
    monkeypatch.setitem(sys.modules, "hid", hid)
    monkeypatch.setenv("BLINKA_MCP2221_RESET_DELAY", "-1")
    monkeypatch.setenv("BLINKA_MCP2221_HID_DELAY", "0")
    module = load_source("_test_mcp2221_led_backend", "mcp2221.py")
    try:
        yield module.mcp2221, device
    finally:
        atexit.unregister(module.mcp2221.close)
        module.mcp2221.close()


@pytest.mark.parametrize("pin_id,_mode_name,raw_name", LED_CASES)
def test_sram_mode_change_preserves_other_gp_settings(
    real_backend, pin_id, _mode_name, raw_name
):
    backend, device = real_backend
    backend.gpio_set_pin(0, 1)
    backend.gpio_set_direction(1, 0)
    backend.gpio_set_pin(1, 1)
    backend.gp_set_mode(2, backend.GP_ALT1)
    expected_settings = [0x18, 0x10, 0x03, 0x08]
    assert backend._gp_config == expected_settings
    device.commands.clear()

    raw_mode = getattr(backend, raw_name)
    backend.gp_set_mode(pin_id, raw_mode)
    expected_settings[pin_id] = raw_mode
    report = bytearray(64)
    report[0] = 0x60
    report[3] = 0x80
    report[5] = 0x80
    report[7] = 0xFF
    report[8:12] = expected_settings
    expected_reports = [b"\x61" + bytes(63), bytes(report)]
    assert device.commands == expected_reports
    assert backend._gp_config == expected_settings

    backend.gp_set_mode(pin_id, raw_mode)
    assert device.commands == expected_reports
    assert backend._gp_config == expected_settings
