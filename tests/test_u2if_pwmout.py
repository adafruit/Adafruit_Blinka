# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Exercise U2IF PWM cleanup without board detection or physical HID access."""

import gc
import importlib.util
from pathlib import Path
import subprocess
import sys
import textwrap
from types import ModuleType, SimpleNamespace
import weakref

import pytest

# Pytest supplies named fixtures; the fixture inspects resource ownership.
# pylint: disable=redefined-outer-name,protected-access

SOURCE = (
    Path(__file__).resolve().parents[1]
    / "src/adafruit_blinka/microcontroller/rp2040_u2if/pwmio.py"
)


class RecordingBackend:
    """Inert backend that can fail after beginning configuration or cleanup."""

    def __init__(self):
        self.events = []
        self.active = False
        self.configure_error = None
        self.deinit_error = None
        self.frequency = 500
        self.duty_cycle = 0

    def pwm_configure(self, pin, **options):
        """Model partially initialized output before a configuration failure."""
        self.events.append(("configure", pin, options))
        self.active = True
        if self.configure_error is not None:
            raise self.configure_error
        self.frequency = options["frequency"]
        self.duty_cycle = options["duty_cycle"]

    def pwm_deinit(self, pin):
        """Record every cleanup attempt, including failures."""
        self.events.append(("deinit", pin))
        if self.deinit_error is not None:
            raise self.deinit_error
        self.active = False

    def pwm_get_frequency(self, pin):
        """Return the fake frequency."""
        self.events.append(("get_frequency", pin))
        return self.frequency

    def pwm_set_frequency(self, pin, value):
        """Update the fake frequency."""
        self.events.append(("set_frequency", pin, value))
        self.frequency = value

    def pwm_get_duty_cycle(self, pin):
        """Return the fake duty cycle."""
        self.events.append(("get_duty_cycle", pin))
        return self.duty_cycle

    def pwm_set_duty_cycle(self, pin, value):
        """Update the fake duty cycle."""
        self.events.append(("set_duty_cycle", pin, value))
        self.duty_cycle = value


@pytest.fixture
def pwm_driver(monkeypatch):
    """Import only the PWM wrapper and detach all test-owned finalizers."""
    backend = RecordingBackend()
    package_name = "_test_u2if_pwmout"
    bridge_name = f"{package_name}.rp2040_u2if"
    package = ModuleType(package_name)
    package.__path__ = []
    bridge = ModuleType(bridge_name)
    bridge.rp2040_u2if = backend
    monkeypatch.setitem(sys.modules, package_name, package)
    monkeypatch.setitem(sys.modules, bridge_name, bridge)
    spec = importlib.util.spec_from_file_location(f"{package_name}.pwmio", SOURCE)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)

    finalizers = []
    real_finalize = module.finalize

    def tracked_finalize(*args, **kwargs):
        finalizer = real_finalize(*args, **kwargs)
        finalizers.append(finalizer)
        return finalizer

    monkeypatch.setattr(module, "finalize", tracked_finalize)
    try:
        yield SimpleNamespace(
            PWMOut=module.PWMOut,
            backend=backend,
            pin=SimpleNamespace(id=1),
            finalizers=finalizers,
        )
    finally:
        for finalizer in finalizers:
            finalizer.detach()


def test_configuration_and_live_properties(pwm_driver):
    pwm = pwm_driver.PWMOut(
        pwm_driver.pin, frequency=1200, duty_cycle=123, variable_frequency=True
    )
    assert pwm_driver.backend.events == [
        (
            "configure",
            pwm_driver.pin,
            {"frequency": 1200, "duty_cycle": 123, "variable_frequency": True},
        )
    ]
    assert pwm.frequency == 1200
    assert pwm.duty_cycle == 123
    pwm.frequency = 2400
    pwm.duty_cycle = 456
    assert pwm.frequency == 2400
    assert pwm.duty_cycle == 456
    pwm.deinit()
    assert not pwm_driver.backend.active


def test_explicit_deinit_is_once_even_after_collection(pwm_driver):
    pwm = pwm_driver.PWMOut(pwm_driver.pin)
    reference = weakref.ref(pwm)
    pwm_driver.backend.events.clear()
    pwm.deinit()
    pwm.deinit()
    del pwm
    gc.collect()
    assert reference() is None
    assert pwm_driver.backend.events == [("deinit", pwm_driver.pin)]


def test_collection_releases_pwm_without_strong_self_reference(pwm_driver):
    pwm = pwm_driver.PWMOut(pwm_driver.pin)
    reference = weakref.ref(pwm)
    pwm_driver.backend.events.clear()
    del pwm
    gc.collect()
    assert reference() is None
    assert pwm_driver.backend.events == [("deinit", pwm_driver.pin)]
    assert not pwm_driver.backend.active


@pytest.mark.parametrize("body_fails", [False, True])
def test_context_manager_cleanup(pwm_driver, body_fails):
    def use_pwm():
        with pwm_driver.PWMOut(pwm_driver.pin) as pwm:
            assert pwm_driver.backend.active
            assert pwm.frequency == 500
            pwm_driver.backend.events.clear()
            if body_fails:
                raise LookupError("context body failed")

    if body_fails:
        with pytest.raises(LookupError, match="context body failed"):
            use_pwm()
    else:
        use_pwm()
    gc.collect()
    assert pwm_driver.backend.events == [("deinit", pwm_driver.pin)]
    assert not pwm_driver.backend.active


@pytest.mark.parametrize("error_type", [RuntimeError, KeyboardInterrupt])
@pytest.mark.parametrize("rollback_fails", [False, True])
def test_configuration_failure_rolls_back_and_preserves_error(
    pwm_driver, error_type, rollback_fails
):
    original = error_type("configuration failed")
    pwm_driver.backend.configure_error = original
    if rollback_fails:
        pwm_driver.backend.deinit_error = OSError("rollback failed")
    with pytest.raises(error_type) as caught:
        pwm_driver.PWMOut(pwm_driver.pin)
    assert caught.value is original
    assert [event[0] for event in pwm_driver.backend.events] == [
        "configure",
        "deinit",
    ]
    assert len(pwm_driver.finalizers) == 1
    assert not pwm_driver.finalizers[0].alive
    if not rollback_fails:
        assert not pwm_driver.backend.active


@pytest.mark.parametrize("name", ["frequency", "duty_cycle"])
@pytest.mark.parametrize("write", [False, True])
def test_properties_reject_deinitialized_pwm(pwm_driver, name, write):
    pwm = pwm_driver.PWMOut(pwm_driver.pin)
    pwm.deinit()
    pwm_driver.backend.events.clear()
    with pytest.raises(ValueError, match="deinitialized"):
        if write:
            setattr(pwm, name, 100)
        else:
            getattr(pwm, name)
    assert pwm_driver.backend.events == []


def test_failed_cleanup_is_not_retried(pwm_driver):
    pwm = pwm_driver.PWMOut(pwm_driver.pin)
    pwm_driver.backend.events.clear()
    original = OSError("cleanup failed")
    pwm_driver.backend.deinit_error = original
    with pytest.raises(OSError) as caught:
        pwm.deinit()
    assert caught.value is original
    pwm.deinit()
    del pwm
    gc.collect()
    assert pwm_driver.backend.events == [("deinit", pwm_driver.pin)]
    assert not pwm_driver.finalizers[0].alive


@pytest.mark.parametrize("lifetime", ["global", "live_container", "cycle"])
def test_process_exit_disables_pwm_before_hid_finalizers(lifetime):
    """Model cython-hidapi's native-close finalizer, without native pointers."""
    script = textwrap.dedent(
        """
        import gc
        import importlib.util
        import sys
        from types import ModuleType, SimpleNamespace
        import weakref

        gc.disable()
        # Any accidental production backend import must fail, not access USB.
        sys.modules["board"] = None
        sys.modules["hid"] = None
        state = {"closed": False, "active": False}

        class Token:
            pass

        def library_exit():
            assert state["closed"], "HID library exited before native close"
            print("hid-exit", flush=True)

        def native_close():
            assert not state["active"], "PWM output remained enabled at HID close"
            state["closed"] = True
            print("hid-close", flush=True)

        library = Token()
        weakref.finalize(library, library_exit)
        device = Token()
        weakref.finalize(device, native_close)

        class Backend:
            def __init__(self):
                self.device = device

            def pwm_configure(self, pin, **options):
                state["active"] = True

            def pwm_deinit(self, pin):
                assert not state["closed"], "PWM accessed a freed HID handle"
                state["active"] = False
                print("pwm-deinit", flush=True)

        package = ModuleType("_exit_u2if_pwmout")
        package.__path__ = []
        bridge = ModuleType(package.__name__ + ".rp2040_u2if")
        bridge.rp2040_u2if = Backend()
        sys.modules[package.__name__] = package
        sys.modules[bridge.__name__] = bridge
        spec = importlib.util.spec_from_file_location(
            package.__name__ + ".pwmio", sys.argv[1]
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        pwm = module.PWMOut(SimpleNamespace(id=1))
        if sys.argv[2] == "live_container":
            live = [pwm]
            del pwm
        elif sys.argv[2] == "cycle":
            pwm.cycle = pwm
            del pwm
        print("ready", flush=True)
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", script, str(SOURCE), lifetime],
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
    assert result.stdout.splitlines() == [
        "ready",
        "pwm-deinit",
        "hid-close",
        "hid-exit",
    ]
