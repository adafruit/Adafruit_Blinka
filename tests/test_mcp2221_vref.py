# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""MCP2221 pin-mux reference preservation with an inert HID transport."""

import atexit
import importlib.util
import sys
from collections import deque
from pathlib import Path
from types import ModuleType

import pytest

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name
# The GP cache is part of the state whose preservation this regression covers.
# pylint: disable=protected-access

SOURCE = (
    Path(__file__).parents[1] / "src/adafruit_blinka/microcontroller/mcp2221/mcp2221.py"
)


def hid_frame(command):
    """Include the report ID and padding used by the physical HID protocol."""
    return b"\x00" + command + bytes(64 - len(command))


def sram_response(dac=0, adc=0):
    """Encode references separately from the power-up DAC and IRQ bits."""
    response = bytearray(64)
    response[0] = 0x61
    response[6] = (dac << 5) | 0x1B
    response[7] = (adc << 2) | 0xE3
    return response


class InertHID:
    """Record complete production reports without enumerating or opening USB."""

    def __init__(self):
        self.frames = []
        self.responses = None
        self.write_error = None
        self.opened = False

    def open(self, vendor_id, product_id):
        """Validate device selection without accessing any native library."""
        assert (vendor_id, product_id) == (0x04D8, 0x00DD)
        self.opened = True

    def close(self):
        """No physical resource exists to release."""
        self.opened = False

    def write(self, frame):
        """Record the report, optionally reproducing a native write failure."""
        assert self.opened
        assert len(frame) == 65
        assert frame[0] == 0
        self.frames.append(bytes(frame))
        if self.write_error is not None:
            raise self.write_error
        return len(frame)

    def read(self, length):
        """Supply valid initialization responses or an explicit test scenario."""
        assert self.opened
        assert length == 64
        if self.responses is None:
            response = bytearray(64)
            response[0] = self.frames[-1][1]
            return response
        assert self.responses, "driver requested an unexpected response"
        response = self.responses.popleft()
        if isinstance(response, Exception):
            raise response
        return response

    def script(self, *responses):
        """Remove initialization reports and select subsequent read results."""
        self.frames.clear()
        self.responses = deque(responses)


@pytest.fixture
def backend(monkeypatch):
    """Import only the production backend with reset disabled and inert HID."""
    device = InertHID()
    hid = ModuleType("hid")
    hid.device = lambda: device
    monkeypatch.setitem(sys.modules, "hid", hid)
    monkeypatch.setenv("BLINKA_MCP2221_RESET_DELAY", "-1")
    monkeypatch.setenv("BLINKA_MCP2221_HID_DELAY", "0")
    spec = importlib.util.spec_from_file_location("_test_mcp2221_vref", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        yield module.mcp2221, device
    finally:
        atexit.unregister(module.mcp2221.close)
        module.mcp2221.close()


@pytest.mark.parametrize("dac", range(8))
@pytest.mark.parametrize("adc", range(8))
def test_mode_change_explicitly_replays_both_references(backend, dac, adc):
    """All reference encodings survive, without copying unrelated SRAM fields."""
    mcp, device = backend
    settings = [0x18, 0x10, 0x03, 0x08]
    mcp._gp_config = settings.copy()
    pin = (dac + adc) % 4
    mode = (mcp.GP_ALT0, mcp.GP_ALT1, mcp.GP_ALT0, mcp.GP_DEDICATED)[pin]
    device.script(sram_response(dac, adc), b"\x60" + bytes(63))

    mcp.gp_set_mode(pin, mode)

    settings[pin] = mode
    expected = bytearray(64)
    expected[0] = 0x60
    expected[3] = 0x80 | dac
    expected[5] = 0x80 | adc
    expected[7] = 0xFF
    expected[8:12] = settings
    assert device.frames == [hid_frame(b"\x61"), hid_frame(expected)]
    assert mcp._gp_config == settings
    assert not device.responses


def test_repeated_mode_does_not_read_or_write_sram(backend):
    """A no-op retains the existing direction/output bits without a transfer."""
    mcp, device = backend
    settings = [0x18, 0x10, 0x03, 0x08]
    mcp._gp_config = settings.copy()
    device.script()

    mcp.gp_set_mode(0, mcp.GP_GPIO)

    assert not device.frames
    assert mcp._gp_config == settings


@pytest.mark.parametrize("length", [0, 1, 2, 7, 8, 63, 65])
def test_incomplete_or_oversized_sram_response_stops_before_write(backend, length):
    """Do not act on partial or malformed reports, even if fields are present."""
    response = bytearray(length)
    if response:
        response[0] = 0x61
    assert_failed_sram_read_preserves_configuration(backend, response)


@pytest.mark.parametrize("echo", [0x00, 0x60, 0xFF])
def test_wrong_sram_command_echo_stops_before_write(backend, echo):
    """A response from another command cannot supply reference settings."""
    response = sram_response(5, 3)
    response[0] = echo
    assert_failed_sram_read_preserves_configuration(backend, response)


@pytest.mark.parametrize("status", [1, 0xFF])
def test_failed_sram_status_stops_before_write(backend, status):
    """Do not replace references when the device could not retrieve them."""
    response = sram_response(5, 3)
    response[1] = status
    assert_failed_sram_read_preserves_configuration(backend, response)


def assert_failed_sram_read_preserves_configuration(backend, response):
    """An unsuccessful read cannot update the GP cache or send Set SRAM."""
    mcp, device = backend
    original = mcp._gp_config.copy()
    device.script(response)

    with pytest.raises(OSError):
        mcp.gp_set_mode(0, mcp.GP_ALT0)

    assert device.frames == [hid_frame(b"\x61")]
    assert mcp._gp_config == original
    assert not device.responses


@pytest.mark.parametrize("phase", ["write", "read"])
def test_native_sram_transfer_error_propagates_unchanged(backend, phase):
    """Keep the original transport error and leave the pending mode untouched."""
    mcp, device = backend
    original = mcp._gp_config.copy()
    error = OSError("native HID failure")
    if phase == "write":
        device.script()
        device.write_error = error
    else:
        device.script(error)

    with pytest.raises(OSError) as raised:
        mcp.gp_set_mode(0, mcp.GP_ALT0)

    assert raised.value is error
    assert device.frames == [hid_frame(b"\x61")]
    assert mcp._gp_config == original
    assert not device.responses
