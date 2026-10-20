# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Confirmed GPIO cache updates with production code and an inert HID transport."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

# Pytest supplies the named fixtures; assertions inspect the confirmed cache.
# pylint: disable=redefined-outer-name,protected-access,too-many-arguments

SOURCE = (
    Path(__file__).parents[1] / "src/adafruit_blinka/microcontroller/mcp2221/mcp2221.py"
)
SETTERS = [
    pytest.param("gp_set_mode", 0x18, 2, 0x02, id="mode"),
    pytest.param("gpio_set_direction", 0x10, 1, 0x18, id="input"),
    pytest.param("gpio_set_direction", 0x18, 0, 0x10, id="output"),
    pytest.param("gpio_set_pin", 0x08, 1, 0x18, id="high"),
    pytest.param("gpio_set_pin", 0x18, 0, 0x08, id="low"),
]


class RecordingHID:
    """Inject a native failure on a selected command, after any reference read."""

    def __init__(self):
        self.events = []
        self.last_command = None
        self.failure_command = None
        self.failure_phase = None
        self.failure = None
        self.observe_cache = lambda: None
        self.opened = False

    def open(self, vendor_id, product_id):
        """Never enumerate or open a physical USB device."""
        assert (vendor_id, product_id) == (0x04D8, 0x00DD)
        self.opened = True

    def close(self):
        """There are no physical resources to release."""
        self.opened = False

    def fail(self, phase, otherwise):
        """Consume one injected result without recovering the driver session."""
        self.observe_cache()
        if self.failure_command == self.last_command and self.failure_phase == phase:
            self.failure_phase = None
            if isinstance(self.failure, BaseException):
                raise self.failure  # pylint: disable=raising-bad-type
            return self.failure
        return otherwise

    def write(self, frame):
        """Record attempted reports and normally return the native byte count."""
        assert self.opened
        assert len(frame) == 65
        assert frame[0] == 0
        self.last_command = frame[1]
        self.events.append(("write", bytes(frame)))
        return self.fail("write", len(frame))

    def read(self, length):
        """Return complete matching replies, including nonzero references."""
        assert self.opened
        assert length == 64
        self.events.append(("read", length))
        report = bytearray(64)
        report[0] = self.last_command
        if self.last_command == 0x61:
            report[6] = (5 << 5) | 0x1B
            report[7] = (3 << 2) | 0xE3
        return self.fail("read", report)

    def sleep(self, delay):
        """Exercise the real post-write interruption point without waiting."""
        self.events.append(("sleep", delay))
        return self.fail("sleep", None)

    def commands(self):
        """Return outgoing commands without their zero HID report IDs."""
        return [event[1][1:] for event in self.events if event[0] == "write"]


@pytest.fixture
def backend(monkeypatch):
    """Import only production code with inert HID and isolated exit handlers."""
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
    spec = importlib.util.spec_from_file_location("_test_mcp2221_gpio_cache", SOURCE)
    module = importlib.util.module_from_spec(spec)
    with monkeypatch.context() as imports:
        imports.setitem(sys.modules, "hid", hid)
        imports.setitem(sys.modules, "atexit", isolated_atexit)
        spec.loader.exec_module(module)
    module.time = SimpleNamespace(sleep=device.sleep)
    assert exit_handlers == [module.mcp2221.close]
    device.events.clear()
    try:
        yield module.mcp2221, device
    finally:
        for callback in exit_handlers:
            callback()
        exit_handlers.clear()


def expected_commands(operation, pin, argument, config):
    """Build reference-preserving SRAM or GPIO reports, excluding report IDs."""
    report = bytearray(64)
    if operation == "gp_set_mode":
        report[0] = 0x60
        report[3] = 0x85
        report[5] = 0x83
        report[7] = 0xFF
        report[8:12] = config
        return [b"\x61" + bytes(63), bytes(report)]
    report[0] = 0x50
    offset = 4 * (pin + 1) if operation == "gpio_set_direction" else 2 + 4 * pin
    report[offset] = 1
    report[offset + 1] = argument
    return [bytes(report)]


def watch_confirmed_cache(driver, device, before):
    """Every native operation must still see the last confirmed state."""

    def observe():
        assert driver._gp_config == before

    device.observe_cache = observe


def assert_gpio_blocked(driver, device, before):
    """Old/new modes and other GPIO requests cannot reuse an uncertain session."""
    events = list(device.events)
    operations = [
        ("gp_set_mode", 2, before[2] & 0x07),
        ("gp_set_mode", 2, driver.GP_ALT0),
        ("gp_set_mode", 3, driver.GP_ALT1),
        ("gpio_set_direction", 1, 0),
        ("gpio_set_direction", 1, 1),
        ("gpio_set_pin", 1, 0),
        ("gpio_set_pin", 1, 1),
    ]
    for operation, pin, argument in operations:
        with pytest.raises(OSError) as raised:
            getattr(driver, operation)(pin, argument)
        message = str(raised.value).lower()
        assert "reconnect" in message and "restart" in message
        assert driver._gp_config == before
        assert driver._hid_in_sync is False
        assert device.events == events


@pytest.mark.parametrize("operation,initial,argument,updated", SETTERS)
def test_success_commits_cache_after_complete_exchange(
    backend, operation, initial, argument, updated
):
    driver, device = backend
    before = [0x10, 0x08, initial, 0x18]
    driver._gp_config = list(before)
    watch_confirmed_cache(driver, device, before)

    assert getattr(driver, operation)(2, argument) is None

    after = list(before)
    after[2] = updated
    assert driver._gp_config == after
    assert driver._hid_in_sync is True
    assert device.commands() == expected_commands(operation, 2, argument, after)


@pytest.mark.parametrize("operation,initial,argument,updated", SETTERS)
@pytest.mark.parametrize("phase", ["write", "sleep", "read"])
@pytest.mark.parametrize("error_type", [OSError, KeyboardInterrupt])
def test_native_failure_preserves_cache_and_blocks_all_gpio(
    backend, operation, initial, argument, updated, phase, error_type
):
    driver, device = backend
    before = [0x10, 0x08, initial, 0x18]
    driver._gp_config = list(before)
    watch_confirmed_cache(driver, device, before)
    device.failure_command = 0x60 if operation == "gp_set_mode" else 0x50
    device.failure_phase = phase
    device.failure = error_type("injected native interruption")

    with pytest.raises(error_type) as raised:
        getattr(driver, operation)(2, argument)

    assert raised.value is device.failure
    assert driver._gp_config == before
    after = list(before)
    after[2] = updated
    # In mode tests the reference read succeeds before the actual 0x60 fails.
    assert device.commands() == expected_commands(operation, 2, argument, after)
    assert_gpio_blocked(driver, device, before)


@pytest.mark.parametrize("operation,initial,argument,updated", SETTERS)
@pytest.mark.parametrize("count", [0, 64])
def test_incomplete_native_write_preserves_cache_and_blocks_gpio(
    backend, operation, initial, argument, updated, count
):
    driver, device = backend
    before = [0x10, 0x08, initial, 0x18]
    driver._gp_config = list(before)
    watch_confirmed_cache(driver, device, before)
    device.failure_command = 0x60 if operation == "gp_set_mode" else 0x50
    device.failure_phase = "write"
    device.failure = count

    with pytest.raises(OSError, match="incomplete"):
        getattr(driver, operation)(2, argument)

    after = list(before)
    after[2] = updated
    assert device.commands() == expected_commands(operation, 2, argument, after)
    assert device.events[-1][0] == "write"
    assert_gpio_blocked(driver, device, before)


@pytest.mark.parametrize("reply", [b"", b"\x60" + bytes(62), b"\x50" + bytes(63)])
def test_invalid_set_sram_reply_preserves_mode_cache(backend, reply):
    driver, device = backend
    before = [0x10, 0x08, 0x18, 0x18]
    driver._gp_config = list(before)
    watch_confirmed_cache(driver, device, before)
    device.failure_command = 0x60
    device.failure_phase = "read"
    device.failure = reply

    with pytest.raises(OSError, match="Invalid"):
        driver.gp_set_mode(2, driver.GP_ALT0)

    assert [command[0] for command in device.commands()] == [0x61, 0x60]
    assert_gpio_blocked(driver, device, before)


def test_unrelated_i2c_fault_blocks_cached_mode_shortcut(backend):
    driver, device = backend
    before = [0x10, 0x08, 0x18, 0x18]
    driver._gp_config = list(before)
    device.failure_command = 0x10
    device.failure_phase = "read"
    device.failure = OSError("unrelated I2C status read failed")

    with pytest.raises(OSError) as raised:
        driver._i2c_status()

    assert raised.value is device.failure
    assert_gpio_blocked(driver, device, before)


def test_mode_noop_keeps_direction_and_output_bits(backend):
    driver, device = backend
    before = [0x10, 0x08, 0x18, 0x00]
    driver._gp_config = list(before)

    assert driver.gp_set_mode(2, driver.GP_GPIO) is None

    assert driver._gp_config == before
    assert driver._hid_in_sync is True
    assert device.events == []


@pytest.mark.parametrize(
    "operation,argument", [("gpio_set_direction", 1), ("gpio_set_pin", 0)]
)
def test_unchanged_gpio_setting_still_transfers(backend, operation, argument):
    driver, device = backend
    before = [0x10, 0x08, 0x08, 0x00]
    driver._gp_config = list(before)

    assert getattr(driver, operation)(2, argument) is None

    assert driver._gp_config == before
    assert driver._hid_in_sync is True
    assert device.commands() == expected_commands(operation, 2, argument, before)
