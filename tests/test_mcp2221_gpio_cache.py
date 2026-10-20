# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""GPIO cache commits with the production MCP2221 driver and inert HID transport."""

import atexit
import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name,too-many-arguments

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
    """Inject one native failure before a write or after an accepted write."""

    def __init__(self):
        self.commands = []
        self.failure_phase = None
        self.failure = OSError("injected HID transport error")
        self.opened = False

    def open(self, vendor_id, product_id):
        """Never enumerate or open a physical USB device."""
        assert (vendor_id, product_id) == (0x04D8, 0x00DD)
        self.opened = True

    def close(self):
        """There are no physical resources to release."""
        self.opened = False

    def write(self, report):
        """Record accepted writes, not those which raise first."""
        assert self.opened
        assert len(report) == 65
        assert report[0] == 0
        if self.failure_phase == "write":
            self.failure_phase = None
            raise self.failure
        self.commands.append(bytes(report[1:]))

    def read(self, length):
        """A read error leaves actual hardware state deliberately unspecified."""
        assert self.opened
        assert length == 64
        if self.failure_phase == "read":
            self.failure_phase = None
            raise self.failure
        return bytearray(64)


@pytest.fixture
def backend(monkeypatch):
    """Import only this backend with fake HID and unregister its exit handler."""
    device = RecordingHID()
    hid = ModuleType("hid")
    hid.device = lambda: device
    monkeypatch.setitem(sys.modules, "hid", hid)
    monkeypatch.setenv("BLINKA_MCP2221_RESET_DELAY", "-1")
    monkeypatch.setenv("BLINKA_MCP2221_HID_DELAY", "0")
    spec = importlib.util.spec_from_file_location("_test_mcp2221_gpio_cache", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.time = SimpleNamespace(sleep=lambda _delay: None)
    device.commands.clear()
    try:
        yield module.mcp2221, device
    finally:
        atexit.unregister(module.mcp2221.close)
        module.mcp2221.close()


def expected_report(operation, pin, argument, config):
    """Build the unchanged command layout, excluding the zero HID report ID."""
    report = bytearray(64)
    if operation == "gp_set_mode":
        report[0] = 0x60
        report[7] = 0xFF
        report[8:12] = config
    else:
        report[0] = 0x50
        offset = 4 * (pin + 1) if operation == "gpio_set_direction" else 2 + 4 * pin
        report[offset] = 1
        report[offset + 1] = argument
    return bytes(report)


@pytest.mark.parametrize("operation,initial,argument,updated", SETTERS)
@pytest.mark.parametrize("phase", ["write", "read"])
def test_failed_transfer_preserves_cache_and_retry(
    backend, operation, initial, argument, updated, phase
):
    driver, device = backend
    before = [0x10, 0x08, initial, 0x18]
    driver._gp_config = list(before)  # pylint: disable=protected-access
    device.failure_phase = phase

    with pytest.raises(OSError) as raised:
        getattr(driver, operation)(2, argument)

    assert raised.value is device.failure
    assert driver._gp_config == before  # pylint: disable=protected-access
    assert driver._gp_config_dirty is True  # pylint: disable=protected-access
    assert len(device.commands) == (1 if phase == "read" else 0)

    device.commands.clear()
    assert getattr(driver, operation)(2, argument) is None
    after = list(before)
    after[2] = updated
    assert driver._gp_config == after  # pylint: disable=protected-access
    # A successful direction/value write cannot confirm the whole SRAM cache.
    assert driver._gp_config_dirty is (  # pylint: disable=protected-access
        operation != "gp_set_mode"
    )
    assert device.commands == [expected_report(operation, 2, argument, after)]


@pytest.mark.parametrize("operation,initial,argument,updated", SETTERS)
@pytest.mark.parametrize("phase", ["write", "read"])
def test_other_pin_mode_does_not_replay_failed_setting(
    backend, operation, initial, argument, updated, phase
):
    # The failed request must not become an unrelated pin's later SRAM replay.
    assert initial != updated
    driver, device = backend
    before = [0x10, 0x08, initial, 0x18]
    driver._gp_config = list(before)  # pylint: disable=protected-access
    device.failure_phase = phase
    with pytest.raises(OSError):
        getattr(driver, operation)(2, argument)

    device.commands.clear()
    driver.gp_set_mode(3, driver.GP_ALT1)
    after = list(before)
    after[3] = driver.GP_ALT1
    assert device.commands == [expected_report("gp_set_mode", 3, driver.GP_ALT1, after)]
    assert driver._gp_config == after  # pylint: disable=protected-access


@pytest.mark.parametrize("operation,initial,argument,updated", SETTERS)
@pytest.mark.parametrize("phase", ["write", "read"])
def test_old_mode_is_replayed_after_uncertain_transfer(
    backend, operation, initial, argument, updated, phase
):
    # A read failure can occur after the device has accepted a NEW setting.
    assert initial != updated
    driver, device = backend
    before = [0x10, 0x08, initial, 0x18]
    driver._gp_config = list(before)  # pylint: disable=protected-access
    device.failure_phase = phase
    with pytest.raises(OSError):
        getattr(driver, operation)(2, argument)

    device.commands.clear()
    old_mode = initial & 0x07
    assert driver.gp_set_mode(2, old_mode) is None
    after = list(before)
    assert device.commands == [expected_report("gp_set_mode", 2, old_mode, after)]
    assert driver._gp_config == after  # pylint: disable=protected-access
    assert driver._gp_config_dirty is False  # pylint: disable=protected-access

    # Only the confirmed full replay makes the same-mode shortcut safe again.
    device.commands.clear()
    assert driver.gp_set_mode(2, old_mode) is None
    assert device.commands == []


@pytest.mark.parametrize("phase", ["write", "read"])
@pytest.mark.parametrize(
    "operation,argument,updated",
    [("gpio_set_direction", 0, 0), ("gpio_set_pin", 1, 0x18)],
)
def test_partial_gpio_success_keeps_mode_replay_required(
    backend, phase, operation, argument, updated
):
    driver, device = backend
    before = [0x10, 0x08, 0x18, 0x18]
    driver._gp_config = list(before)  # pylint: disable=protected-access
    device.failure_phase = phase
    with pytest.raises(OSError):
        driver.gp_set_mode(2, driver.GP_ALT0)

    # A successful operation on another pin does not resolve the lost reply.
    getattr(driver, operation)(1, argument)
    after_partial = list(before)
    after_partial[1] = updated
    assert driver._gp_config == after_partial  # pylint: disable=protected-access
    assert driver._gp_config_dirty is True  # pylint: disable=protected-access

    device.commands.clear()
    driver.gp_set_mode(2, driver.GP_GPIO)
    after_replay = list(after_partial)
    assert device.commands == [
        expected_report("gp_set_mode", 2, driver.GP_GPIO, after_replay)
    ]
    assert driver._gp_config == after_replay  # pylint: disable=protected-access
    assert driver._gp_config_dirty is False  # pylint: disable=protected-access


@pytest.mark.parametrize("phase", ["write", "read"])
def test_failed_recovery_replay_remains_dirty(backend, phase):
    driver, device = backend
    before = [0x10, 0x08, 0x18, 0x18]
    driver._gp_config = list(before)  # pylint: disable=protected-access
    device.failure_phase = "read"
    with pytest.raises(OSError):
        driver.gp_set_mode(2, driver.GP_ALT0)

    device.failure_phase = phase
    with pytest.raises(OSError) as raised:
        driver.gp_set_mode(2, driver.GP_GPIO)
    assert raised.value is device.failure
    assert driver._gp_config == before  # pylint: disable=protected-access
    assert driver._gp_config_dirty is True  # pylint: disable=protected-access

    device.commands.clear()
    driver.gp_set_mode(2, driver.GP_GPIO)
    after = list(before)
    assert device.commands == [expected_report("gp_set_mode", 2, driver.GP_GPIO, after)]
    assert driver._gp_config_dirty is False  # pylint: disable=protected-access


@pytest.mark.parametrize("phase", ["write", "read"])
@pytest.mark.parametrize(
    "operation,argument",
    [("gp_set_mode", 2), ("gpio_set_direction", 0), ("gpio_set_pin", 1)],
)
def test_interruption_preserves_cache_and_requires_replay(
    backend, phase, operation, argument
):
    driver, device = backend
    before = [0x08] * 4
    driver._gp_config = list(before)  # pylint: disable=protected-access
    device.failure = KeyboardInterrupt()
    device.failure_phase = phase
    with pytest.raises(KeyboardInterrupt) as raised:
        getattr(driver, operation)(2, argument)
    assert raised.value is device.failure
    assert driver._gp_config == before  # pylint: disable=protected-access
    assert driver._gp_config_dirty is True  # pylint: disable=protected-access

    device.commands.clear()
    driver.gp_set_mode(2, driver.GP_GPIO)
    assert device.commands == [expected_report("gp_set_mode", 2, 0, before)]
    assert driver._gp_config_dirty is False  # pylint: disable=protected-access


def test_mode_noop_keeps_direction_and_output_bits(backend):
    driver, device = backend
    before = [0x10, 0x08, 0x18, 0x00]
    driver._gp_config = list(before)  # pylint: disable=protected-access
    assert driver.gp_set_mode(2, driver.GP_GPIO) is None
    assert driver._gp_config == before  # pylint: disable=protected-access
    assert device.commands == []


@pytest.mark.parametrize(
    "operation,argument", [("gpio_set_direction", 1), ("gpio_set_pin", 0)]
)
def test_unchanged_gpio_setting_still_transfers(backend, operation, argument):
    driver, device = backend
    before = [0x10, 0x08, 0x08, 0x00]
    driver._gp_config = list(before)  # pylint: disable=protected-access
    assert getattr(driver, operation)(2, argument) is None
    assert driver._gp_config == before  # pylint: disable=protected-access
    assert device.commands == [expected_report(operation, 2, argument, before)]
