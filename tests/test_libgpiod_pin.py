# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Shared libgpiod lifecycle and digitalio regressions, without GPIO hardware."""

# Recording fakes and assertions intentionally inspect each backend's handles.
# pylint: disable=redefined-outer-name,protected-access

import sys
from types import ModuleType

import pytest

from test_raspberry_pi_pin import SOURCE, load_source, make_pin


@pytest.fixture(params=["2", "1", "legacy"])
def generic_pins(monkeypatch, request):
    module, state, library = make_pin(
        monkeypatch,
        version="2" if request.param == "2" else "1",
        backend="libgpiod_pin",
        legacy=request.param == "legacy",
    )
    # Generic SBC GPIO controllers must not be mistaken for Pi header controllers.
    state.devices = {0: ("non-pi-controller", 64), 6: ("another-sbc", 128)}
    return module, state, library


def line_handle(pin):
    return getattr(pin, "_line_request", None) or getattr(pin, "_line", None)


def configured_output(configuration, library):
    if isinstance(configuration, dict):
        return configuration["type"] == 2
    return configuration.direction is library.line.Direction.OUTPUT


def configured_bias(configuration):
    if isinstance(configuration, dict):
        return configuration["flags"]
    return configuration.bias


def expected_bias(library, direction):
    if getattr(library, "__version__", "1.x").startswith("2."):
        return getattr(library.line.Bias, direction)
    suffix = "DISABLE" if direction == "DISABLED" else direction
    if hasattr(library, "LINE_REQ_DIR_IN"):
        return getattr(library, "LINE_REQ_FLAG_BIAS_" + suffix)
    return getattr(library.line_request, "FLAG_BIAS_" + suffix)


@pytest.mark.parametrize("identity,chip_index", [(18, 0), ((6, 18), 6)])
def test_generic_constructor_keeps_ids_and_defers_non_pi_hardware(
    generic_pins, identity, chip_index
):
    module, state, _ = generic_pins
    pin = module.Pin(identity)
    assert pin.id == identity
    assert repr(pin) == str(identity) and pin == identity
    assert pin == module.Pin(identity)
    assert not state.chips and not state.requests
    pin.init(mode=pin.OUT)
    assert pin.id == identity and state.chips[-1].index == chip_index
    assert line_handle(pin).offset == 18
    pin.deinit()
    pin.deinit()
    assert all(chip.close_calls == 1 for chip in state.chips)


def test_2x_generic_tuple_accepts_device_path(monkeypatch):
    module, state, _ = make_pin(monkeypatch, backend="libgpiod_pin")
    identity = ("/dev/gpiochip6", 18)
    pin = module.Pin(identity)
    assert pin.id == identity and not state.chips
    pin.init()
    assert state.chips[-1].path == "/dev/gpiochip6"
    assert pin.id == identity and line_handle(pin).offset == 18
    pin.deinit()


def test_generic_instances_own_independent_handles_and_reopen(generic_pins):
    module, state, _ = generic_pins
    first, second = module.Pin((6, 18)), module.Pin((6, 23))
    first.init(mode=first.OUT)
    second.init(mode=second.OUT)
    chip1, chip2 = first._chip, second._chip
    request1, request2 = line_handle(first), line_handle(second)
    assert chip1 is not chip2 and request1 is not request2
    first.value(1)
    assert first.value() == 1 and second.value() == 0
    first.deinit()
    assert chip1.closed and not request1.live
    assert not chip2.closed and request2.live
    first.init(mode=first.OUT)
    assert first._chip is not chip1 and line_handle(first) is not request1
    assert first.id == (6, 18) and first._chip.index == 6
    assert first.value() == 1
    second.deinit()
    first.deinit()
    assert all(chip.closed for chip in state.chips)


def test_input_none_and_explicit_none_clear_previous_pulls(generic_pins):
    module, _, library = generic_pins
    pin = module.Pin(18)
    pin.init(pull=pin.PULL_UP)
    request = line_handle(pin)
    pin.init(pull=pin.PULL_DOWN)
    pin.init(pull=None)
    pin.init(pull=pin.PULL_NONE)
    assert [configured_bias(config) for config in request.configurations] == [
        expected_bias(library, "PULL_UP"),
        expected_bias(library, "PULL_DOWN"),
        expected_bias(library, "DISABLED"),
        expected_bias(library, "DISABLED"),
    ]
    pin.init(mode=None, pull=pin.PULL_UP)
    assert configured_bias(request.configurations[-1]) == expected_bias(
        library, "PULL_UP"
    )
    assert pin._mode == pin.IN
    pin.deinit()


def test_no_mode_no_pull_does_not_reconfigure_existing_output(generic_pins):
    module, _, _ = generic_pins
    pin = module.Pin(18)
    pin.init(mode=pin.OUT)
    pin.value(1)
    request = line_handle(pin)
    count = len(request.configurations)
    pin.init(mode=None)
    assert pin._mode == pin.OUT and pin.value() == 1
    assert len(request.configurations) == count
    pin.deinit()


def test_output_reconfiguration_retains_high_and_low(generic_pins):
    module, _, library = generic_pins
    pin = module.Pin(18)
    pin.init(pull=pin.PULL_UP)
    pin.init(mode=pin.OUT)
    request = line_handle(pin)
    for value in (1, 0, 1):
        pin.value(value)
        pin.init(mode=pin.OUT)
        assert pin.value() == value
        configuration = request.configurations[-1]
        assert configured_output(configuration, library)
        if isinstance(configuration, dict):
            if hasattr(library, "LINE_REQ_DIR_OUT"):
                assert configuration["default_vals"] == [value]
            else:
                assert configuration["default_val"] == value
        else:
            assert configuration.bias is library.line.Bias.DISABLED
            assert configuration.output_value.value == value
    pin.deinit()


def test_failed_value_write_does_not_change_commanded_output(generic_pins):
    module, state, _ = generic_pins
    pin = module.Pin(18)
    pin.init(mode=pin.OUT)
    pin.value(1)
    state.fail_write = True
    with pytest.raises(OSError, match="write failed"):
        pin.value(0)
    assert pin._value == 1
    state.fail_write = False
    pin.init(mode=pin.OUT)
    assert pin.value() == 1
    other = module.Pin(23)
    other.init(mode=other.OUT)
    assert other._value == 0 and other.value() == 0
    pin.deinit()
    other.deinit()


@pytest.mark.parametrize("pull", [1, 2, 0])
def test_output_rejects_all_explicit_pull_values_and_cleans_ownership(
    generic_pins, pull
):
    module, state, _ = generic_pins
    pin = module.Pin(18)
    pin.init()
    with pytest.raises(RuntimeError, match="Cannot set pull resistor"):
        pin.init(mode=pin.OUT, pull=pull)
    assert pin._chip is None and line_handle(pin) is None
    assert all(chip.closed for chip in state.chips)
    assert all(not request.live for request in state.requests)


def test_pull_only_configuration_uses_cached_output_mode(generic_pins):
    module, state, _ = generic_pins
    pin = module.Pin(18)
    pin.init(mode=pin.OUT)
    pin.value(1)
    with pytest.raises(RuntimeError, match="Cannot set pull resistor"):
        pin.init(mode=None, pull=pin.PULL_UP)
    assert pin._mode == pin.OUT and pin._value == 1
    assert pin._chip is None and line_handle(pin) is None
    assert all(chip.closed for chip in state.chips)


@pytest.mark.parametrize("failure", ["open", "request", "invalid_mode", "invalid_pull"])
def test_shared_failed_setup_releases_owned_resources(generic_pins, failure):
    module, state, _ = generic_pins
    pin = module.Pin((6, 18))
    arguments = {}
    if failure == "open":
        state.fail_open = 1
    elif failure == "request":
        state.fail_request = True
    elif failure == "invalid_mode":
        arguments["mode"] = 99
    else:
        arguments["pull"] = 99
    with pytest.raises((OSError, RuntimeError)):
        pin.init(**arguments)
    assert pin.id == (6, 18) and pin._chip is None and line_handle(pin) is None
    assert all(chip.closed for chip in state.chips)
    assert all(not request.live for request in state.requests)
    pin.deinit()
    pin.__del__()  # pylint: disable=unnecessary-dunder-call


def test_2x_configuration_failure_keeps_primary_error_and_previous_mode(monkeypatch):
    module, state, _ = make_pin(monkeypatch, backend="libgpiod_pin")
    pin = module.Pin(18)
    pin.init()
    state.fail_config = state.fail_release = state.fail_close = True
    with pytest.raises(OSError, match="configuration failed"):
        pin.init(mode=pin.OUT)
    assert pin._mode == pin.IN
    assert pin._chip is None and line_handle(pin) is None
    assert state.chips[-1].closed and not state.requests[-1].live
    pin.deinit()


def test_request_error_wins_over_chip_cleanup_error(generic_pins):
    module, state, _ = generic_pins
    pin = module.Pin(18)
    state.fail_request = state.fail_close = True
    with pytest.raises(OSError, match="request failed"):
        pin.init()
    assert pin._chip is None and line_handle(pin) is None
    assert all(chip.closed for chip in state.chips)
    assert all(not request.live for request in state.requests)
    pin.deinit()


@pytest.mark.parametrize("legacy", [False, True])
def test_1x_failed_input_request_keeps_previous_successful_mode(monkeypatch, legacy):
    module, state, _ = make_pin(
        monkeypatch, version="1", backend="libgpiod_pin", legacy=legacy
    )
    pin = module.Pin(18)
    pin.init(mode=pin.OUT)
    pin.value(1)
    state.fail_request = True
    with pytest.raises(OSError, match="request failed"):
        pin.init(mode=pin.IN)
    assert pin._mode == pin.OUT and pin._value == 1
    assert pin._chip is None and line_handle(pin) is None
    assert all(chip.closed for chip in state.chips)
    state.fail_request = False
    pin.init(mode=pin.OUT)
    assert pin.value() == 1
    pin.deinit()


def test_cleanup_attempts_line_and_chip_once_when_both_raise(generic_pins):
    module, state, _ = generic_pins
    first, second = module.Pin(18), module.Pin(23)
    first.init()
    second.init()
    chip1, chip2 = first._chip, second._chip
    request1, request2 = line_handle(first), line_handle(second)
    release_calls = request1.release_calls
    state.fail_release = state.fail_close = True
    with pytest.raises(OSError, match="release failed"):
        first.deinit()
    assert request1.release_calls == release_calls + 1 and chip1.close_calls == 1
    assert first._chip is None and line_handle(first) is None
    assert not chip2.closed and request2.live
    first.deinit()
    assert request1.release_calls == release_calls + 1 and chip1.close_calls == 1
    state.fail_release = state.fail_close = False
    second.deinit()


@pytest.mark.parametrize("legacy", [False, True])
def test_1x_missing_bias_disable_only_rejects_explicit_request(monkeypatch, legacy):
    module, state, library = make_pin(
        monkeypatch, version="1", backend="libgpiod_pin", legacy=legacy
    )
    if legacy:
        del library.line_request.FLAG_BIAS_DISABLE
    else:
        del library.LINE_REQ_FLAG_BIAS_DISABLE
    pin = module.Pin(18)
    pin.init()
    assert line_handle(pin).configurations[-1]["flags"] == 0
    pin.init(mode=pin.OUT)
    pin.value(1)
    pin.init(mode=pin.OUT)
    assert pin.value() == 1
    with pytest.raises(NotImplementedError):
        pin.init(mode=pin.IN, pull=pin.PULL_NONE)
    assert pin._chip is None and line_handle(pin) is None
    assert all(chip.closed for chip in state.chips)


def test_actual_digitalio_switch_to_high_survives_drive_mode_configuration(
    generic_pins, monkeypatch
):
    module, state, _ = generic_pins
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.board_id = "NON_PI_GPIOD_BOARD"
    importing = ModuleType("adafruit_blinka.importing")
    importing.get_import_file = lambda name, _location: SOURCE / name
    importing.import_microcontroller = lambda namespace, *_args: namespace.update(
        Pin=module.Pin
    )
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    monkeypatch.setitem(sys.modules, "adafruit_blinka.importing", importing)
    digitalio = load_source("_generic_digitalio_test", SOURCE / "digitalio.py")
    original = module.Pin((6, 18))
    digital = digitalio.DigitalInOut(original)
    assert original._chip is None and digital._pin.id == original.id
    digital.switch_to_input(pull=digitalio.Pull.UP)
    digital.pull = None
    digital.switch_to_output(value=True)
    assert digital.value is True
    digital.drive_mode = digitalio.DriveMode.PUSH_PULL
    assert digital.value is True
    digital.switch_to_output(value=False)
    assert digital.value is False
    digital.deinit()
    assert all(chip.closed for chip in state.chips)
