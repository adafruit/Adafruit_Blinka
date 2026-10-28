# SPDX-FileCopyrightText: 2026 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Check MCP2222 buffer handling and GPIO without USB hardware."""

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest
from pymcp2222 import GpioVal, IODirection
from pymcp2222.exceptions import I2CAddressNackError, I2CError


@pytest.fixture(name="backend")
def mcp2222_backend(monkeypatch):
    device = SimpleNamespace(i2c=Mock(), io=Mock())
    package = "adafruit_blinka.microcontroller.mcp2222"
    monkeypatch.setitem(
        sys.modules, package + ".mcp2222", SimpleNamespace(mcp2222=device)
    )
    modules = []
    for name in ("i2c", "pin"):
        path = Path(__file__).parents[1] / "src" / Path(*package.split("."))
        spec = importlib.util.spec_from_file_location(
            package + "." + name, path / (name + ".py")
        )
        module = importlib.util.module_from_spec(spec)
        monkeypatch.setitem(sys.modules, spec.name, module)
        spec.loader.exec_module(module)
        modules.append(module)
    return device, modules[0].I2C(), modules[1].Pin


def test_probe_and_write_slice(backend):
    device, i2c, _ = backend
    i2c.writeto(0x44, b"")
    i2c.writeto(0x44, b"abcd", start=1, end=3)
    assert device.i2c.write.call_args_list == [call(0x44, b"\x00"), call(0x44, b"bc")]


@pytest.mark.parametrize("stop", [False, True])
def test_combined_transfer_slices(backend, stop):
    device, i2c, _ = backend
    device.i2c.read.return_value = device.i2c.write_read.return_value = b"xy"
    buffer = bytearray(b"----")
    i2c.writeto_then_readfrom(
        0x44,
        b"abcd",
        buffer,
        out_start=1,
        out_end=3,
        in_start=1,
        in_end=3,
        stop=stop,
    )
    assert buffer == b"-xy-"
    if stop:
        assert device.i2c.method_calls[-2:] == [
            call.write(0x44, b"bc"),
            call.read(0x44, 2),
        ]
        device.i2c.write_read.assert_not_called()
    else:
        device.i2c.write_read.assert_called_once_with(0x44, b"bc", 2)
        device.i2c.write.assert_not_called()


def test_read_slice_and_empty_read(backend):
    device, i2c, _ = backend
    device.i2c.read.return_value = b"xy"
    buffer = bytearray(b"----")
    i2c.readfrom_into(0x44, buffer, start=1, end=3)
    i2c.readfrom_into(0x44, bytearray())
    assert buffer == b"-xy-"
    device.i2c.read.assert_called_once_with(0x44, 2)


def test_scan_does_not_hide_bus_failures(backend):
    device, i2c, _ = backend
    device.i2c.write.side_effect = lambda address, data: (
        None if address == 0x44 else _nack()
    )
    assert i2c.scan() == [0x44]
    device.i2c.write.side_effect = I2CError("bus failure")
    with pytest.raises(OSError, match="bus failure"):
        i2c.scan()
    with pytest.raises(OSError, match="bus failure"):
        i2c.writeto(0x44, b"x")


def _nack():
    raise I2CAddressNackError("NACK")


def test_gpio_reconfiguration_preserves_output(backend):
    device, _, pin_class = backend
    pin = pin_class(0)
    pin.init(pin.OUT)
    pin.value(1)
    pin.init(pin.OUT)
    config = device.io.set_config.call_args.args[1]
    assert config.direction == IODirection.OUTPUT
    assert config.open_drain is False
    assert config.idle_state is True
    device.io.gpio_read.return_value = GpioVal.HIGH
    assert pin.value() == 1
    device.io.gpio_write.assert_called_once_with(0, 1)
    pin.init(pin.IN, pull=pin.PULL_UP)
    assert device.io.set_config.call_args.args[1].pull_up is True
    with pytest.raises(AttributeError, match="Not an output"):
        pin.value(0)
    with pytest.raises(NotImplementedError, match="Open-drain"):
        pin.init(pin.OPEN_DRAIN)


def test_dedicated_i2c_pin_is_not_gpio(backend):
    _, _, pin_class = backend
    with pytest.raises(ValueError, match="Not an MCP2222 GPIO"):
        pin_class().init()
