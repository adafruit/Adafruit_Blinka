# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""MCP2221 command/reply synchronization using an inert HID transport."""

import importlib.util
import sys
from collections import deque
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name,protected-access

SOURCE = (
    Path(__file__).parents[1] / "src/adafruit_blinka/microcontroller/mcp2221/mcp2221.py"
)
RESET = b"\x70\xab\xcd\xef"


def reply(command=0x10, *, result=0, state=0):
    """Build a complete reply with the command echo and I2C status fields."""
    report = bytearray(64)
    report[0] = command
    report[1] = result
    report[2] = state
    report[8] = state
    return report


class RecordingHID:
    """Accept initialization and permit independent write and read failures."""

    def __init__(self):
        self.opened = False
        self.events = []
        self.last_command = None
        self.writes = deque()
        self.reads = None
        self.sleep_error = None

    def open(self, vendor_id, product_id):
        """Assert the production device identifiers without opening USB."""
        assert (vendor_id, product_id) == (0x04D8, 0x00DD)
        self.opened = True

    def close(self):
        """There is no native handle or physical device."""
        self.opened = False

    def write(self, report):
        """Record complete outgoing reports and return hidapi's byte count."""
        assert self.opened
        assert len(report) == 65
        assert report[0] == 0
        self.events.append(("write", bytes(report)))
        self.last_command = report[1]
        result = self.writes.popleft() if self.writes else 65
        if isinstance(result, BaseException):
            raise result  # pylint: disable=raising-bad-type
        return result

    def read(self, length):
        """A scripted interruption leaves any following reply queued."""
        assert self.opened
        assert length == 64
        self.events.append(("read", length))
        if self.reads is None:
            return reply(self.last_command)
        assert self.reads, "driver requested an unexpected response"
        result = self.reads.popleft()
        if isinstance(result, BaseException):
            raise result
        return result

    def sleep(self, delay):
        """Record the post-write delay without waiting."""
        self.events.append(("sleep", delay))
        if self.sleep_error is not None:
            raise self.sleep_error

    def script(self, *, writes=(), reads=None):
        """Discard only initialization history, never perform HID operations."""
        self.events.clear()
        self.writes = deque(writes)
        self.reads = None if reads is None else deque(reads)
        self.sleep_error = None


@pytest.fixture
def backend(monkeypatch):
    """Import the actual backend without native HID or live exit callbacks."""
    device = RecordingHID()
    hid = ModuleType("hid")
    hid.device = lambda: device
    exit_handlers = []
    isolated_atexit = ModuleType("atexit")

    def register(callback):
        exit_handlers.append(callback)
        return callback

    isolated_atexit.register = register
    monkeypatch.setenv("BLINKA_MCP2221_RESET_DELAY", "-1")
    monkeypatch.setenv("BLINKA_MCP2221_HID_DELAY", "0")
    spec = importlib.util.spec_from_file_location("_test_mcp2221_hid", SOURCE)
    module = importlib.util.module_from_spec(spec)
    with monkeypatch.context() as imports:
        imports.setitem(sys.modules, "hid", hid)
        imports.setitem(sys.modules, "atexit", isolated_atexit)
        spec.loader.exec_module(module)
    module.time = SimpleNamespace(sleep=device.sleep)
    module.MCP2221_RETRY_MAX = 3
    assert exit_handlers == [module.mcp2221.close]
    device.script()
    try:
        yield module, device
    finally:
        for callback in exit_handlers:
            callback()
        exit_handlers.clear()


def assert_tainted_and_blocked(chip, device):
    """An uncertain stream must not send or consume another command/reply."""
    assert chip._hid_in_sync is False  # pylint: disable=protected-access
    events = list(device.events)
    with pytest.raises(OSError) as caught:
        chip._hid_xfer(b"\x10")  # pylint: disable=protected-access
    message = str(caught.value).lower()
    assert "reconnect" in message
    assert "restart" in message
    assert device.events == events


@pytest.mark.parametrize("command", [b"\x10", bytes(range(64)), bytearray(b"\x61")])
@pytest.mark.parametrize("container", [bytes, bytearray, list])
def test_complete_matching_reply_confirms_stream(backend, command, container):
    module, device = backend
    chip = module.mcp2221
    assert chip._hid_in_sync is True  # pylint: disable=protected-access
    report = container(reply(command[0]))
    device.script(reads=[report])
    result = chip._hid_xfer(command)  # pylint: disable=protected-access
    assert result == report
    assert chip._hid_in_sync is True  # pylint: disable=protected-access
    assert device.events == [
        ("write", b"\0" + bytes(command) + b"\0" * (64 - len(command))),
        ("sleep", 0),
        ("read", 64),
    ]


@pytest.mark.parametrize("command", [b"", bytes(65)])
def test_invalid_command_length_is_rejected_before_io(backend, command):
    module, device = backend
    with pytest.raises(ValueError):
        module.mcp2221._hid_xfer(command)  # pylint: disable=protected-access
    assert device.events == []
    assert module.mcp2221._hid_in_sync is True  # pylint: disable=protected-access


def test_stream_is_tainted_before_calling_native_write(backend, monkeypatch):
    module, device = backend
    native_write = device.write

    def write(report):
        assert module.mcp2221._hid_in_sync is False
        return native_write(report)

    monkeypatch.setattr(device, "write", write)
    module.mcp2221._hid_xfer(b"\x10")
    assert module.mcp2221._hid_in_sync is True


@pytest.mark.parametrize("count", [None, -1, 0, 1, 64, 66, 65.0, "65", True])
def test_incomplete_or_invalid_write_never_reads(backend, count):
    module, device = backend
    pending = reply()
    device.script(writes=[count], reads=[pending])
    with pytest.raises(OSError):
        module.mcp2221._hid_xfer(b"\x10")  # pylint: disable=protected-access
    assert [event[0] for event in device.events] == ["write"]
    assert list(device.reads) == [pending]
    assert_tainted_and_blocked(module.mcp2221, device)


@pytest.mark.parametrize("phase", ["write", "sleep", "read"])
@pytest.mark.parametrize("error_type", [OSError, RuntimeError, KeyboardInterrupt])
def test_native_exception_identity_and_taint(backend, phase, error_type):
    module, device = backend
    error = error_type("native transfer interruption")
    pending = reply()
    device.script(
        writes=[error] if phase == "write" else [],
        reads=[error, pending] if phase == "read" else [pending],
    )
    if phase == "sleep":
        device.sleep_error = error
    with pytest.raises(error_type) as caught:
        module.mcp2221._hid_xfer(b"\x10")  # pylint: disable=protected-access
    assert caught.value is error
    assert list(device.reads) == [pending]
    assert_tainted_and_blocked(module.mcp2221, device)


@pytest.mark.parametrize(
    "report", [[], [0x10], [0x10] + [0] * 62, [0x10] + [0] * 64, reply(0x61)]
)
def test_incomplete_or_wrong_command_reply_taints_stream(backend, report):
    module, device = backend
    device.script(reads=[report])
    with pytest.raises(OSError):
        module.mcp2221._hid_xfer(b"\x10")  # pylint: disable=protected-access
    assert [event[0] for event in device.events] == ["write", "sleep", "read"]
    assert_tainted_and_blocked(module.mcp2221, device)


@pytest.mark.parametrize("result", [0, 1, 0x41, 0x7F, 0xFF])
def test_matching_semantic_failure_is_not_transport_failure(backend, result):
    module, device = backend
    report = reply(result=result, state=0x25)
    device.script(reads=[report])
    assert (
        module.mcp2221._hid_xfer(b"\x10") == report
    )  # pylint: disable=protected-access
    assert module.mcp2221._hid_in_sync is True  # pylint: disable=protected-access


def test_same_command_reply_left_after_interruption_is_not_reused(backend):
    module, device = backend
    chip = module.mcp2221
    stale = reply(0x60)
    interrupted = KeyboardInterrupt("read interrupted before consuming reply")
    device.script(reads=[interrupted, stale])
    with pytest.raises(KeyboardInterrupt) as caught:
        chip._hid_xfer(b"\x60\x00")  # pylint: disable=protected-access
    assert caught.value is interrupted
    events = list(device.events)
    with pytest.raises(OSError):
        chip._hid_xfer(b"\x60\x01")  # pylint: disable=protected-access
    assert device.events == events
    assert list(device.reads) == [stale]


def test_failed_retry_cannot_consume_a_previously_queued_reply(backend):
    module, device = backend
    chip = module.mcp2221
    stale = reply(0x60)
    device.script(writes=[65, 0], reads=[KeyboardInterrupt(), stale])
    with pytest.raises(KeyboardInterrupt):
        chip._hid_xfer(b"\x60")  # pylint: disable=protected-access
    events = list(device.events)
    with pytest.raises(OSError):
        chip._hid_xfer(b"\x60")  # pylint: disable=protected-access
    assert device.events == events
    assert list(device.writes) == [0]
    assert list(device.reads) == [stale]


@pytest.mark.parametrize(
    "command,response",
    [(b"\x10", False), (b"\x70", False), (RESET + b"\0", False), (RESET, True)],
)
def test_only_exact_reset_may_omit_response(backend, command, response):
    module, device = backend
    with pytest.raises(ValueError):
        module.mcp2221._hid_xfer(
            command, response=response
        )  # pylint: disable=protected-access
    assert device.events == []
    assert module.mcp2221._hid_in_sync is True  # pylint: disable=protected-access


def test_exact_reset_writes_without_reading(backend):
    module, device = backend
    device.script(reads=[])
    assert (
        module.mcp2221._hid_xfer(RESET, response=False) is None
    )  # pylint: disable=protected-access
    assert [event[0] for event in device.events] == ["write", "sleep"]
    assert module.mcp2221._hid_in_sync is True  # pylint: disable=protected-access


@pytest.mark.parametrize("failure", [OSError("HID write failed"), 64])
def test_scan_propagates_transport_failure_without_probing_more_addresses(
    backend, failure
):
    module, device = backend
    device.script(writes=[failure])
    with pytest.raises(OSError) as caught:
        module.mcp2221.i2c_scan(start=8, end=10)
    if isinstance(failure, OSError):
        assert caught.value is failure
    assert [event[0] for event in device.events] == ["write"]
    assert_tainted_and_blocked(module.mcp2221, device)


def test_scan_retains_complete_nack_compatibility(backend):
    module, device = backend
    successful = [reply(0x10), reply(0x90), reply(0x10), reply(0x10)]
    device.script(
        reads=successful
        + [reply(0x10), reply(0x90, result=1, state=module.RESP_ADDR_NACK)]
        + successful
    )
    assert module.mcp2221.i2c_scan(start=8, end=10) == [8, 10]
    assert module.mcp2221._hid_in_sync is True  # pylint: disable=protected-access
    addresses = [
        event[1][4] >> 1
        for event in device.events
        if event[0] == "write" and event[1][1] == 0x90
    ]
    assert addresses == [8, 9, 10]


def test_complete_status_error_leaves_transport_usable(backend):
    module, device = backend
    device.script(reads=[reply(result=1), reply()])
    with pytest.raises(OSError, match="Couldn't get I2C status"):
        module.mcp2221._i2c_status()  # pylint: disable=protected-access
    assert module.mcp2221._hid_in_sync is True  # pylint: disable=protected-access
    assert module.mcp2221._i2c_status() == reply()  # pylint: disable=protected-access
