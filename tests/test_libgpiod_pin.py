# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Shared libgpiod lifecycle and digitalio regressions, without GPIO hardware."""

# Recording fakes and assertions intentionally inspect each backend's handles.
# pylint: disable=redefined-outer-name,protected-access

import errno
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


def configured_value(configuration):
    if isinstance(configuration, dict):
        if "default_vals" in configuration:
            return configuration["default_vals"][0]
        return configuration["default_val"]
    return configuration.output_value.value


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


def record_1x_requests(monkeypatch, library, reject):
    """Record both request APIs before modeling a kernel-side rejection."""
    chip_class = library.Chip if hasattr(library, "Chip") else library.chip
    original_get_line = chip_class.get_line
    attempts = []

    def get_line(chip, offset):
        line = original_get_line(chip, offset)
        original_request = line.request

        if hasattr(library, "LINE_REQ_DIR_IN"):

            def request(**arguments):
                assert "default_val" not in arguments
                attempts.append(arguments.copy())
                reject(arguments, len(attempts))
                return original_request(**arguments)

        else:

            def request(config, default_val=0):
                arguments = {
                    "consumer": config.consumer,
                    "type": config.request_type,
                    "flags": config.flags,
                    "default_val": default_val,
                }
                attempts.append(arguments)
                reject(arguments, len(attempts))
                return original_request(config, default_val=default_val)

        monkeypatch.setattr(line, "request", request)
        return line

    monkeypatch.setattr(chip_class, "get_line", get_line)
    return attempts


def reject_kernel_bias(arguments, _attempt):
    """Linux 5.4's linehandle_create rejects unknown bias flags with EINVAL."""
    if arguments["flags"]:
        raise OSError(errno.EINVAL, "unsupported request flags")


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


@pytest.mark.parametrize("pull", [None, 2])
def test_successful_input_clears_cached_output_before_next_output(generic_pins, pull):
    module, _, library = generic_pins
    pin = module.Pin(18)
    pin.init(mode=pin.OUT)
    pin.value(1)
    pin.init(mode=pin.IN, pull=pull)
    assert pin._mode == pin.IN and pin._value == 0
    pin.init(mode=pin.OUT)
    configuration = line_handle(pin).configurations[-1]
    assert configured_output(configuration, library)
    assert configured_value(configuration) == 0 and pin.value() == 0
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


def test_2x_failed_input_configuration_keeps_output_value_for_reopening(monkeypatch):
    module, state, library = make_pin(monkeypatch, backend="libgpiod_pin")
    pin = module.Pin(18)
    pin.init(mode=pin.OUT)
    pin.value(1)
    state.fail_config = True
    with pytest.raises(OSError, match="configuration failed"):
        pin.init(mode=pin.IN)
    assert pin._mode == pin.OUT and pin._value == 1
    assert pin._chip is None and line_handle(pin) is None
    state.fail_config = False
    pin.init(mode=pin.OUT)
    configuration = line_handle(pin).configurations[-1]
    assert configured_output(configuration, library)
    assert configured_value(configuration) == 1 and pin.value() == 1
    pin.deinit()
    assert all(chip.closed for chip in state.chips)


def test_request_error_wins_over_chip_cleanup_error(generic_pins):
    module, state, library = generic_pins
    pin = module.Pin(18)
    state.fail_request = state.fail_close = True
    with pytest.raises(OSError, match="request failed"):
        pin.init()
    is_1x = getattr(library, "__version__", "1.x").startswith("1.")
    assert line_handle(pin) is None
    if is_1x:
        assert pin._chip is state.chips[-1]
    else:
        assert pin._chip is None
    assert all(chip.closed for chip in state.chips)
    assert all(not request.live for request in state.requests)
    state.fail_close = False
    pin.deinit()
    assert pin._chip is None
    assert state.chips[-1].close_calls == (2 if is_1x else 1)


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


def test_cleanup_failure_retains_1x_handles_and_keeps_other_pin_independent(
    generic_pins,
):
    module, state, library = generic_pins
    first, second = module.Pin(18), module.Pin(23)
    first.init()
    second.init()
    chip1, chip2 = first._chip, second._chip
    request1, request2 = line_handle(first), line_handle(second)
    release_calls = request1.release_calls
    state.fail_release = state.fail_close = True
    with pytest.raises(OSError, match="release failed"):
        first.deinit()
    is_1x = getattr(library, "__version__", "1.x").startswith("1.")
    assert request1.release_calls == release_calls + 1
    if is_1x:
        assert first._chip is chip1 and line_handle(first) is request1
        assert chip1.close_calls == 0
    else:
        assert first._chip is None and line_handle(first) is None
        assert chip1.close_calls == 1
    assert not chip2.closed and request2.live
    state.fail_release = state.fail_close = False
    first.deinit()
    assert request1.release_calls == release_calls + (2 if is_1x else 1)
    assert chip1.close_calls == 1
    assert first._chip is None and line_handle(first) is None
    second.deinit()


@pytest.mark.parametrize("legacy", [False, True])
def test_1x_chip_cleanup_retry_does_not_repeat_successful_line_release(
    monkeypatch, legacy
):
    module, state, _ = make_pin(
        monkeypatch, version="1", backend="libgpiod_pin", legacy=legacy
    )
    pin = module.Pin(18)
    pin.init(mode=pin.OUT)
    chip, line = pin._chip, pin._line
    release_calls = line.release_calls
    state.fail_close = True

    with pytest.raises(OSError, match="close failed"):
        pin.deinit()
    assert pin._chip is chip and pin._line is None
    assert chip.close_calls == 1 and line.release_calls == release_calls + 1

    state.fail_close = False
    pin.deinit()
    pin.deinit()
    assert pin._chip is None and pin._line is None
    assert chip.close_calls == 2 and line.release_calls == release_calls + 1


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


@pytest.mark.parametrize("legacy", [False, True])
@pytest.mark.parametrize("mode", [0, 1])
def test_1x_implicit_none_retries_kernel_rejected_bias(monkeypatch, legacy, mode):
    module, state, library = make_pin(
        monkeypatch, version="1", backend="libgpiod_pin", legacy=legacy
    )
    attempts = record_1x_requests(monkeypatch, library, reject_kernel_bias)
    pin = module.Pin(18)
    pin.init(mode=mode)
    assert [attempt["flags"] for attempt in attempts] == [
        expected_bias(library, "DISABLED"),
        0,
    ]
    assert pin._mode == mode and line_handle(pin).live
    assert len(state.chips) == 1 and not state.chips[0].closed
    assert len(state.requests) == 1
    assert len(line_handle(pin).configurations) == 1
    pin.deinit()
    assert state.chips[0].closed and not state.requests[0].live


@pytest.mark.parametrize("legacy", [False, True])
def test_1x_kernel_bias_fallback_preserves_output_value(monkeypatch, legacy):
    module, state, library = make_pin(
        monkeypatch, version="1", backend="libgpiod_pin", legacy=legacy
    )
    attempts = record_1x_requests(monkeypatch, library, reject_kernel_bias)
    pin = module.Pin(18)
    pin.init(mode=pin.OUT)
    for value in (1, 0, 1):
        pin.value(value)
        pin.init(mode=pin.OUT)
        assert pin.value() == value and pin._value == value and pin._mode == pin.OUT
        for attempt in attempts[-2:]:
            assert attempt["consumer"] == "adafruit_blinka"
            if legacy:
                assert attempt["type"] == library.line_request.DIRECTION_OUTPUT
                assert attempt["default_val"] == value
            else:
                assert attempt["type"] == library.LINE_REQ_DIR_OUT
                assert attempt["default_vals"] == [value]
    pin.init(mode=pin.IN)
    assert pin._mode == pin.IN
    pin.deinit()
    assert all(chip.closed for chip in state.chips)


@pytest.mark.parametrize("legacy", [False, True])
def test_1x_successful_input_bias_fallback_clears_cached_output(monkeypatch, legacy):
    module, _, library = make_pin(
        monkeypatch, version="1", backend="libgpiod_pin", legacy=legacy
    )
    attempts = record_1x_requests(monkeypatch, library, reject_kernel_bias)
    pin = module.Pin(18)
    pin.init(mode=pin.OUT)
    pin.value(1)
    pin.init(mode=pin.IN)
    assert [attempt["flags"] for attempt in attempts[-2:]] == [
        expected_bias(library, "DISABLED"),
        0,
    ]
    assert pin._mode == pin.IN and pin._value == 0
    pin.init(mode=pin.OUT)
    assert all(configured_value(attempt) == 0 for attempt in attempts[-2:])
    pin.deinit()


@pytest.mark.parametrize("legacy", [False, True])
@pytest.mark.parametrize("pull", [0, 1, 2])
def test_1x_explicit_bias_requests_do_not_fallback_on_old_kernel(
    monkeypatch, legacy, pull
):
    module, state, library = make_pin(
        monkeypatch, version="1", backend="libgpiod_pin", legacy=legacy
    )
    attempts = record_1x_requests(monkeypatch, library, reject_kernel_bias)
    pin = module.Pin(18)
    with pytest.raises(OSError) as caught:
        pin.init(pull=pull)
    assert caught.value.errno == errno.EINVAL
    assert len(attempts) == 1 and attempts[0]["flags"] != 0
    assert pin._chip is None and line_handle(pin) is None
    assert all(chip.closed for chip in state.chips)
    assert all(not request.live for request in state.requests)


@pytest.mark.parametrize("legacy", [False, True])
@pytest.mark.parametrize(
    "error_number", [errno.EBUSY, errno.EACCES, errno.EIO, errno.EOPNOTSUPP, None]
)
def test_1x_implicit_bias_does_not_retry_unrelated_errors(
    monkeypatch, legacy, error_number
):
    module, state, library = make_pin(
        monkeypatch, version="1", backend="libgpiod_pin", legacy=legacy
    )
    failure = OSError(error_number, "unrelated request failure")

    def reject(_arguments, _attempt):
        raise failure

    attempts = record_1x_requests(monkeypatch, library, reject)
    pin = module.Pin(18)
    with pytest.raises(OSError) as caught:
        pin.init()
    assert caught.value is failure and len(attempts) == 1
    assert pin._chip is None and line_handle(pin) is None
    assert all(chip.closed for chip in state.chips)


@pytest.mark.parametrize("legacy", [False, True])
def test_1x_unbiased_einval_is_not_retried(monkeypatch, legacy):
    module, state, library = make_pin(
        monkeypatch, version="1", backend="libgpiod_pin", legacy=legacy
    )
    if legacy:
        del library.line_request.FLAG_BIAS_DISABLE
    else:
        del library.LINE_REQ_FLAG_BIAS_DISABLE
    failure = OSError(errno.EINVAL, "invalid line")

    def reject(_arguments, _attempt):
        raise failure

    attempts = record_1x_requests(monkeypatch, library, reject)
    pin = module.Pin(18)
    with pytest.raises(OSError) as caught:
        pin.init()
    assert caught.value is failure
    assert len(attempts) == 1 and attempts[0]["flags"] == 0
    assert all(chip.closed for chip in state.chips)


@pytest.mark.parametrize("legacy", [False, True])
def test_1x_fallback_failure_is_not_retried_and_cleans_resources(monkeypatch, legacy):
    module, state, library = make_pin(
        monkeypatch, version="1", backend="libgpiod_pin", legacy=legacy
    )
    pin = module.Pin(18)
    pin.init(mode=pin.OUT)
    pin.value(1)
    failure = OSError(errno.EBUSY, "fallback failed")

    def reject(arguments, attempt):
        if attempt == 2:
            raise failure
        reject_kernel_bias(arguments, attempt)

    attempts = record_1x_requests(monkeypatch, library, reject)
    # Reopen to apply the recording wrapper; preserve the last commanded output.
    pin.deinit()
    state.fail_close = True
    with pytest.raises(OSError) as caught:
        pin.init(mode=pin.IN)
    assert caught.value is failure
    assert len(attempts) == 2 and attempts[-1]["flags"] == 0
    assert pin._mode == pin.OUT and pin._value == 1
    assert pin._chip is state.chips[-1] and line_handle(pin) is None
    assert all(chip.closed for chip in state.chips)
    assert all(not request.live for request in state.requests)
    state.fail_close = False
    pin.deinit()
    assert pin._chip is None and state.chips[-1].close_calls == 2


@pytest.mark.parametrize("legacy", [False, True])
def test_actual_digitalio_initializes_on_kernel_without_bias_flags(monkeypatch, legacy):
    module, state, library = make_pin(
        monkeypatch, version="1", backend="libgpiod_pin", legacy=legacy
    )
    attempts = record_1x_requests(monkeypatch, library, reject_kernel_bias)
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.board_id = "NON_PI_GPIOD_BOARD"
    importing = ModuleType("adafruit_blinka.importing")
    importing.get_import_file = lambda name, _location: SOURCE / name
    importing.import_microcontroller = lambda namespace, *_args: namespace.update(
        Pin=module.Pin
    )
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    monkeypatch.setitem(sys.modules, "adafruit_blinka.importing", importing)
    digitalio = load_source("_old_kernel_digitalio_test", SOURCE / "digitalio.py")
    digital = digitalio.DigitalInOut(module.Pin(18))
    assert digital.direction is digitalio.Direction.INPUT and digital.pull is None
    digital.switch_to_output(value=True)
    assert digital.value is True
    digital.drive_mode = digitalio.DriveMode.PUSH_PULL
    assert digital.value is True
    digital.switch_to_input()
    assert digital.direction is digitalio.Direction.INPUT and digital.pull is None
    assert all(attempts[index]["flags"] == 0 for index in range(1, len(attempts), 2))
    digital.deinit()
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


def test_actual_digitalio_input_to_low_never_configures_stale_high(
    generic_pins, monkeypatch
):
    module, state, library = generic_pins
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
    digital = digitalio.DigitalInOut(module.Pin(18))
    digital.switch_to_output(value=True)
    digital.switch_to_input(pull=digitalio.Pull.DOWN)
    request = line_handle(digital._pin)
    start = len(request.configurations)
    digital.switch_to_output(value=False)
    assert digital.value is False
    output_configurations = [
        configuration
        for configuration in request.configurations[start:]
        if configured_output(configuration, library)
    ]
    assert output_configurations
    assert all(configured_value(config) == 0 for config in output_configurations)
    digital.deinit()
    assert all(chip.closed for chip in state.chips)
