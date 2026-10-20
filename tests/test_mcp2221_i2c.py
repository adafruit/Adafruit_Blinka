# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""MCP2221 I2C exception compatibility with scripted, hardware-free HID reports."""

import atexit
import importlib.util
import sys
from collections import deque
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name

SOURCE = (
    Path(__file__).parents[1] / "src/adafruit_blinka/microcontroller/mcp2221/mcp2221.py"
)


def response(*, result=0, state=0, count=0, nack=False, data=b""):
    """Build one MCP2221 response; state/count fields depend on the command."""
    report = bytearray(64)
    report[1] = result
    report[2] = state
    report[3] = count
    report[4 : 4 + len(data)] = data
    report[8] = state
    report[20] = 0x40 if nack else 0
    return report


class ScriptedHID:
    """Inert HID transport which accepts initialization, then enforces a script."""

    def __init__(self):
        self.responses = None
        self.commands = []
        self.opened = False

    def open(self, vendor_id, product_id):
        """Never open a physical device."""
        assert (vendor_id, product_id) == (0x04D8, 0x00DD)
        self.opened = True

    def close(self):
        """No physical resources exist to release."""
        self.opened = False

    def write(self, report):
        """Record the actual HID report produced by the driver."""
        assert self.opened
        assert len(report) == 65
        assert report[0] == 0
        self.commands.append(bytes(report[1:]))
        return len(report)

    def read(self, length):
        """Return the next scripted response or raise a transport error."""
        assert self.opened
        assert length == 64
        if self.responses is None:
            report = response()
            report[0] = self.commands[-1][0]
            return report
        assert self.responses, "driver requested an unexpected response"
        item = self.responses.popleft()
        if isinstance(item, Exception):
            raise item
        item = bytearray(item)
        item[0] = self.commands[-1][0]
        return item

    def script(self, *reports):
        """Start a new transfer scenario without initialization commands."""
        self.commands.clear()
        self.responses = deque(reports)


@pytest.fixture
def backend(monkeypatch):
    """Import production code with inert HID and no reset or real sleeps."""
    device = ScriptedHID()
    hid = ModuleType("hid")
    hid.device = lambda: device
    monkeypatch.setitem(sys.modules, "hid", hid)
    monkeypatch.setenv("BLINKA_MCP2221_RESET_DELAY", "-1")
    monkeypatch.setenv("BLINKA_MCP2221_HID_DELAY", "0")
    spec = importlib.util.spec_from_file_location("_test_mcp2221", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.time = SimpleNamespace(sleep=lambda _delay: None)
    module.MCP2221_RETRY_MAX = 3
    try:
        yield module, device
    finally:
        atexit.unregister(module.mcp2221.close)
        module.mcp2221.close()


@pytest.mark.parametrize("operation", ["i2c_writeto", "i2c_readfrom_into"])
def test_status_failure_is_oserror(backend, operation):
    module, device = backend
    device.script(response(result=1))
    with pytest.raises(OSError, match="Couldn't get I2C status"):
        getattr(module.mcp2221, operation)(0x59, bytearray(1))


@pytest.mark.parametrize("operation", ["i2c_writeto", "i2c_readfrom_into"])
def test_cancel_failure_is_oserror(backend, operation):
    module, device = backend
    device.script(response(state=1), response(result=1))
    with pytest.raises(OSError, match="Couldn't cancel I2C"):
        getattr(module.mcp2221, operation)(0x59, bytearray(1))


@pytest.mark.parametrize("state", [0x12, 0x23, 0x25, 0x44, 0x62])
@pytest.mark.parametrize("phase", ["command", "completion"])
def test_write_terminal_state_is_oserror(backend, state, phase):
    module, device = backend
    reports = [response()]
    if phase == "command":
        reports.append(response(result=1, state=state))
    else:
        reports.extend([response(), response(), response(state=state)])
    device.script(*reports)
    with pytest.raises(OSError, match="Unrecoverable I2C state failure"):
        module.mcp2221.i2c_writeto(0x59, b"\x01")


@pytest.mark.parametrize("phase", ["command", "completion"])
def test_write_retry_exhaustion_is_oserror(backend, phase):
    module, device = backend
    if phase == "command":
        reports = [response()] + [response(result=1)] * module.MCP2221_RETRY_MAX
    else:
        reports = [response(), response(), response()] + [
            response(state=1)
        ] * module.MCP2221_RETRY_MAX
    device.script(*reports)
    with pytest.raises(OSError, match="I2C write error[:,] max retries reached"):
        module.mcp2221.i2c_writeto(0x59, b"\x01")


def test_write_address_nack_remains_oserror(backend):
    module, device = backend
    device.script(response(), response(), response(), response(nack=True))
    with pytest.raises(OSError, match="I2C slave address was NACK'd"):
        module.mcp2221.i2c_writeto(0x59, b"\x01")


@pytest.mark.parametrize("phase", ["command", "fetch"])
def test_read_command_failure_is_oserror(backend, phase):
    module, device = backend
    reports = [response()]
    if phase == "fetch":
        reports.append(response())
    reports.append(response(result=1))
    device.script(*reports)
    with pytest.raises(OSError, match="Unrecoverable I2C read failure"):
        module.mcp2221.i2c_readfrom_into(0x59, bytearray(1))


def test_read_address_nack_is_oserror(backend):
    module, device = backend
    device.script(response(), response(), response(state=module.RESP_ADDR_NACK))
    with pytest.raises(OSError, match="I2C NACK"):
        module.mcp2221.i2c_readfrom_into(0x59, bytearray(1))


@pytest.mark.parametrize("pending", ["partial", "read-error"])
def test_read_retry_exhaustion_is_oserror(backend, pending):
    module, device = backend
    report = (
        response(result=module.RESP_I2C_PARTIALDATA)
        if pending == "partial"
        else response(count=module.RESP_READ_ERR)
    )
    device.script(response(), response(), *[report] * module.MCP2221_RETRY_MAX)
    with pytest.raises(OSError, match="I2C read error: max retries reached"):
        module.mcp2221.i2c_readfrom_into(0x59, bytearray(1))


@pytest.mark.parametrize("phase", ["write", "read"])
def test_combined_transfer_propagates_oserror(backend, phase):
    module, device = backend
    if phase == "write":
        reports = [response(), response(result=1, state=module.RESP_ADDR_NACK)]
    else:
        reports = [
            response(),
            response(),
            response(state=module.RESP_I2C_WRITINGNOSTOP),
            response(state=module.RESP_I2C_WRITINGNOSTOP),
            response(state=module.RESP_I2C_WRITINGNOSTOP),
            response(),
            response(state=module.RESP_ADDR_NACK),
        ]
    device.script(*reports)
    with pytest.raises(OSError):
        module.mcp2221.i2c_writeto_then_readfrom(0x59, b"\x01", bytearray(1))


def test_scan_continues_after_command_nack(backend):
    module, device = backend
    successful_write = [response(), response(), response(), response()]
    device.script(
        *successful_write,
        response(),
        response(result=1, state=module.RESP_ADDR_NACK),
        *successful_write,
    )
    assert module.mcp2221.i2c_scan(start=8, end=10) == [8, 10]
    assert [report[3] for report in device.commands if report[0] == 0x90] == [
        8 << 1,
        9 << 1,
        10 << 1,
    ]


def test_successful_write_preserves_chunking(backend):
    module, device = backend
    device.script(*[response()] * 6)
    data = bytes(range(61))
    assert module.mcp2221.i2c_writeto(0x59, data) is None
    writes = [report for report in device.commands if report[0] == 0x90]
    assert len(writes) == 2
    assert writes[0] == bytes([0x90, 61, 0, 0xB2]) + data[:60]
    assert writes[1][:5] == bytes([0x90, 61, 0, 0xB2, 60])


@pytest.mark.parametrize("combined", [False, True])
def test_successful_read_preserves_data_and_commands(backend, combined):
    module, device = backend
    reports = []
    if combined:
        reports.extend(
            [
                response(),
                response(),
                response(state=module.RESP_I2C_WRITINGNOSTOP),
                response(state=module.RESP_I2C_WRITINGNOSTOP),
            ]
        )
    reports.extend(
        [
            response(state=module.RESP_I2C_WRITINGNOSTOP if combined else 0),
            response(),
            response(state=module.RESP_READ_COMPL, count=3, data=b"abc"),
        ]
    )
    device.script(*reports)
    buffer = bytearray(3)
    if combined:
        result = module.mcp2221.i2c_writeto_then_readfrom(0x59, b"\x01", buffer)
        expected = [0x10, 0x94, 0x10, 0x10, 0x10, 0x93, 0x40]
    else:
        result = module.mcp2221.i2c_readfrom_into(0x59, buffer)
        expected = [0x10, 0x91, 0x40]
    assert result is None
    assert buffer == b"abc"
    assert [report[0] for report in device.commands] == expected


def test_hid_oserror_is_not_replaced(backend):
    module, device = backend
    error = OSError("USB disconnected")
    device.script(error)
    with pytest.raises(OSError) as raised:
        module.mcp2221.i2c_writeto(0x59, b"\x01")
    assert raised.value is error


def test_gpio_configuration_error_remains_runtimeerror(backend):
    module, device = backend
    report = response()
    report[2] = 0xEE
    device.script(report)
    with pytest.raises(RuntimeError, match="Pin is not set for GPIO operation"):
        module.mcp2221.gpio_get_pin(0)
