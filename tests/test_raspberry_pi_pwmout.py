# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Recording-only adapter tests; no board, GPIO, or native engine imports."""

import importlib.util
import sys
import types
from pathlib import Path

import pytest


class FakeNative:
    instances = []
    constructor_error = None
    cleanup_error = None

    def __init__(self, pin, *, frequency, duty_cycle, variable_frequency):
        self.pin = pin
        self.initial = (frequency, duty_cycle, variable_frequency)
        self.events = []
        self._frequency = frequency
        self._duty = duty_cycle
        self.deinit_calls = 0
        self.released = False
        self.frequency_error = None
        self.duty_error = None
        self.read_error = None
        self.instances.append(self)
        if self.constructor_error is not None:
            raise self.constructor_error

    @property
    def frequency(self):
        if self.released:
            raise ValueError("native released")
        if self.read_error is not None:
            raise self.read_error
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        self.events.append(("frequency", value))
        if self.frequency_error is not None:
            raise self.frequency_error
        self._frequency = value

    @property
    def duty_cycle(self):
        return self._duty

    @duty_cycle.setter
    def duty_cycle(self, value):
        self.events.append(("duty", value))
        if self.duty_error is not None:
            raise self.duty_error
        self._duty = value

    def deinit(self):
        self.events.append(("deinit",))
        self.deinit_calls += 1
        self.released = True
        self._duty = 0
        if self.cleanup_error is not None:
            raise self.cleanup_error


@pytest.fixture(name="adapter")
def pwm_adapter_fixture(monkeypatch):
    FakeNative.instances = []
    FakeNative.constructor_error = None
    FakeNative.cleanup_error = None
    package_name = "adafruit_blinka_raspberry_pi_pwm"
    package = types.ModuleType(package_name)
    package.PWMOut = FakeNative
    monkeypatch.setitem(sys.modules, package_name, package)
    path = (
        Path(__file__).resolve().parents[1]
        / "src/adafruit_blinka/microcontroller/generic_linux/raspberry_pi_pwmout.py"
    )
    spec = importlib.util.spec_from_file_location("recording_pwm_adapter", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    yield module
    for native in FakeNative.instances:
        native.read_error = None
        native.frequency_error = None
        native.duty_error = None
    FakeNative.cleanup_error = None


@pytest.mark.parametrize("variable", [False, True])
def test_defaults_real_pin_identity_and_always_writable_frequency(adapter, variable):
    pin = object()
    with adapter.PWMOut(pin, variable_frequency=variable) as output:
        native = FakeNative.instances[-1]
        assert native.pin is pin
        assert native.initial == (500, 0, True)
        assert (output.frequency, output.duty_cycle, output.enabled) == (500, 0, True)
        output.frequency = 50
        assert native.frequency == output.frequency == 50
    assert native.deinit_calls == 1
    assert native.released and native.duty_cycle == 0


@pytest.mark.parametrize(
    "requested, effective",
    [(1, 1), (50.4, 50), (50.5, 50), (50.6, 51), (10000.4, 10000), (25000.2, 25000)],
)
def test_float_frequency_keeps_nominal_readback(adapter, requested, effective):
    with adapter.PWMOut(object(), frequency=requested) as output:
        native = FakeNative.instances[-1]
        assert native.initial[0] == effective
        assert output.frequency == requested
        assert output.period == 1.0 / requested
        output.frequency = requested
        assert native.events == [("frequency", effective)]


@pytest.mark.parametrize("duty", [0, 1, 32767.75, 65534, 65535])
def test_duty_integer_submission_and_endpoint_readbacks(adapter, duty):
    with adapter.PWMOut(object(), duty_cycle=duty) as output:
        native = FakeNative.instances[-1]
        assert native.initial[1] == int(duty)
        assert output.duty_cycle == int(duty)
        output.duty_cycle = duty
        assert native.events == [("duty", int(duty))]


def test_period_delegates_reciprocal_frequency(adapter):
    with adapter.PWMOut(object()) as output:
        output.period = 0.004
        native = FakeNative.instances[-1]
        assert output.frequency == native.frequency == 250
        assert output.period == 0.004
        output.period = 1 / 50.6
        assert output.frequency == pytest.approx(50.6)
        assert native.frequency == 51


def test_disable_keeps_line_and_duty_then_updates_frequency_while_low(adapter):
    with adapter.PWMOut(object(), duty_cycle=32767.75) as output:
        native = FakeNative.instances[-1]
        output.enabled = False
        assert output.enabled is False and native.duty_cycle == 0
        assert output.duty_cycle == 32767
        output.duty_cycle = 4915.9
        assert native.events == [("duty", 0)]
        assert output.duty_cycle == 4915
        output.frequency = 50.6
        assert native.events[-1] == ("frequency", 51)
        assert native.duty_cycle == 0
        assert output.frequency == 50.6
        assert len(FakeNative.instances) == 1 and not native.released
        output.enabled = True
        assert native.events[-1] == ("duty", 4915)
        assert output.enabled is True
    assert native.deinit_calls == 1


def test_enabled_zero_duty_is_not_disabled(adapter):
    with adapter.PWMOut(object()) as output:
        output.duty_cycle = 0
        assert output.enabled is True
        output.enabled = False
        output.duty_cycle = 65535
        output.enabled = True
        assert FakeNative.instances[-1].duty_cycle == 65535


@pytest.mark.parametrize(
    "field, value, error",
    [
        ("frequency", "50", TypeError),
        ("frequency", float("nan"), ValueError),
        ("frequency", float("inf"), ValueError),
        ("frequency", 0.49, ValueError),
        ("frequency", -1, ValueError),
        ("frequency", 1000000000.6, ValueError),
        ("frequency", 10**1000, ValueError),
        ("duty_cycle", "50", TypeError),
        ("duty_cycle", float("nan"), ValueError),
        ("duty_cycle", float("inf"), ValueError),
        ("duty_cycle", -0.1, ValueError),
        ("duty_cycle", 65535.1, ValueError),
    ],
)
def test_invalid_constructor_never_creates_native(adapter, field, value, error):
    with pytest.raises(error):
        adapter.PWMOut(object(), **{field: value})
    assert not FakeNative.instances


@pytest.mark.parametrize(
    "field, value, error",
    [
        ("frequency", "50", TypeError),
        ("frequency", float("nan"), ValueError),
        ("frequency", 0, ValueError),
        ("frequency", 1000000001, ValueError),
        ("duty_cycle", "1", TypeError),
        ("duty_cycle", float("inf"), ValueError),
        ("duty_cycle", -1, ValueError),
        ("duty_cycle", 65536, ValueError),
        ("period", "0.02", TypeError),
        ("period", 0, ValueError),
        ("period", -0.02, ValueError),
        ("period", float("nan"), ValueError),
        ("period", float("inf"), ValueError),
        ("period", 10**1000, ValueError),
        ("enabled", 0, TypeError),
        ("enabled", None, TypeError),
    ],
)
def test_invalid_setter_leaves_public_and_native_state(adapter, field, value, error):
    with adapter.PWMOut(object(), duty_cycle=1234) as output:
        native = FakeNative.instances[-1]
        with pytest.raises(error):
            setattr(output, field, value)
        assert (output.frequency, output.duty_cycle, output.enabled) == (
            500,
            1234,
            True,
        )
        assert (native.frequency, native.duty_cycle, native.events) == (500, 1234, [])


@pytest.mark.parametrize("field", ["frequency", "duty_cycle", "period", "enabled"])
def test_native_setter_errors_do_not_commit_public_cache(adapter, field):
    with adapter.PWMOut(object(), duty_cycle=1234) as output:
        native = FakeNative.instances[-1]
        error = OSError("native configure failed")
        if field in ("frequency", "period"):
            native.frequency_error = error
            value = 50.6 if field == "frequency" else 0.02
        else:
            native.duty_error = error
            value = 9999 if field == "duty_cycle" else False
        with pytest.raises(OSError) as caught:
            setattr(output, field, value)
        assert caught.value is error
        assert (output.frequency, output.duty_cycle, output.enabled) == (
            500,
            1234,
            True,
        )
        assert (native.frequency, native.duty_cycle) == (500, 1234)


def test_enable_error_preserves_disabled_state_and_desired_duty(adapter):
    with adapter.PWMOut(object(), duty_cycle=1234) as output:
        native = FakeNative.instances[-1]
        output.enabled = False
        output.duty_cycle = 9999
        native.duty_error = OSError("cannot enable")
        with pytest.raises(OSError):
            output.enabled = True
        assert output.enabled is False and output.duty_cycle == 9999
        assert native.duty_cycle == 0


def test_disabled_frequency_error_rolls_back_while_output_stays_low(adapter):
    with adapter.PWMOut(object(), duty_cycle=1234) as output:
        native = FakeNative.instances[-1]
        output.enabled = False
        native.frequency_error = OSError("cannot configure")
        with pytest.raises(OSError):
            output.frequency = 50.6
        assert output.frequency == 500 and output.duty_cycle == 1234
        assert output.enabled is False and native.duty_cycle == 0


def test_native_worker_failure_is_not_hidden_by_cached_reads(adapter):
    with adapter.PWMOut(object(), duty_cycle=1234) as output:
        native = FakeNative.instances[-1]
        output.enabled = False
        native.read_error = OSError("worker failed")
        for field in ("frequency", "duty_cycle", "period", "enabled"):
            with pytest.raises(OSError):
                getattr(output, field)
        with pytest.raises(OSError):
            output.duty_cycle = 9999
        # Worker failure must not commit the disabled-state cache.
        assert output._duty_cycle == 1234  # pylint: disable=protected-access


@pytest.mark.parametrize("cleanup_fails", [False, True])
@pytest.mark.parametrize("error_type", [KeyboardInterrupt, OSError])
def test_partial_constructor_cleanup_preserves_original_error(
    adapter, cleanup_fails, error_type
):
    primary = error_type("construction failed")
    FakeNative.constructor_error = primary
    if cleanup_fails:
        FakeNative.cleanup_error = OSError("cleanup failed")
    with pytest.raises(error_type) as caught:
        adapter.PWMOut(object())
    assert caught.value is primary
    native = FakeNative.instances[-1]
    assert native.deinit_calls == 1 and native.released


def test_context_exception_propagates_and_only_its_output_is_released(adapter):
    sibling = adapter.PWMOut(object(), duty_cycle=2222)
    first = adapter.PWMOut(object(), duty_cycle=1111)
    first_native = FakeNative.instances[-1]
    with pytest.raises(RuntimeError, match="caller error"):
        with first as output:
            assert output is first
            raise RuntimeError("caller error")
    assert first_native.deinit_calls == 1
    assert sibling.duty_cycle == 2222 and not FakeNative.instances[0].released
    sibling.deinit()


@pytest.mark.parametrize("cleanup_fails", [False, True])
def test_deinit_repeat_safe_and_all_properties_guarded(adapter, cleanup_fails):
    output = adapter.PWMOut(object())
    native = FakeNative.instances[-1]
    if cleanup_fails:
        FakeNative.cleanup_error = OSError("cleanup failed")
        with pytest.raises(OSError):
            output.deinit()
    else:
        output.deinit()
    output.deinit()
    # Invoke finalization deterministically after explicit release.
    output.__del__()  # pylint: disable=unnecessary-dunder-call
    assert native.deinit_calls == 1
    for field, value in (
        ("frequency", 50),
        ("duty_cycle", 0),
        ("period", 0.02),
        ("enabled", True),
    ):
        with pytest.raises(ValueError, match="deinitialized"):
            setattr(output, field, value)
        with pytest.raises(ValueError, match="deinitialized"):
            getattr(output, field)
    with pytest.raises(ValueError, match="deinitialized"):
        output.__enter__()  # pylint: disable=unnecessary-dunder-call


def test_destructor_suppresses_cleanup_error(adapter):
    output = adapter.PWMOut(object())
    native = FakeNative.instances[-1]
    FakeNative.cleanup_error = OSError("cleanup failed")
    # A direct finalizer call lets its exception suppression be asserted.
    output.__del__()  # pylint: disable=unnecessary-dunder-call
    assert native.deinit_calls == 1


def test_selected_backend_rejects_unsupported_frequency(adapter):
    FakeNative.constructor_error = ValueError("software frequency exceeds 10000 Hz")
    with pytest.raises(ValueError, match="software frequency"):
        adapter.PWMOut(object(), frequency=25000)
    native = FakeNative.instances[-1]
    assert native.initial[0] == 25000
    assert native.released


def test_hardware_cleanup_failure_retains_native_for_retry(adapter, monkeypatch):
    output = adapter.PWMOut(object(), duty_cycle=1234)
    native = FakeNative.instances[-1]
    native.deinitialized = False

    def close():
        native.deinit_calls += 1
        if native.deinit_calls == 1:
            raise OSError("hardware low write failed")
        native.released = True
        native.deinitialized = True

    monkeypatch.setattr(native, "deinit", close)
    with pytest.raises(OSError, match="low write"):
        output.deinit()
    assert output._pwm is native  # pylint: disable=protected-access
    output.deinit()
    output.deinit()
    assert native.deinit_calls == 2
    with pytest.raises(ValueError, match="deinitialized"):
        _ = output.frequency
