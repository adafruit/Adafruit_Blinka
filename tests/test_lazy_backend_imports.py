# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Public annotation imports must not initialize optional GPIO/PWM backends."""

import builtins
import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import get_type_hints

import pytest

import adafruit_blinka
from adafruit_blinka import platform_dependencies

# Keep the isolated import/recording state together; pytest supplies fixtures.
# pylint: disable=redefined-outer-name,protected-access,too-many-locals

ROOT = Path(__file__).parents[1] / "src"
PREFIX = "adafruit_blinka.microcontroller."
NATIVE_PWM = "adafruit_blinka_raspberry_pi_pwm"


class Flags(SimpleNamespace):
    """Avoid running platform detection for unused board/chip selectors."""

    def __getattr__(self, _name):
        return False


def load_module(monkeypatch, name, relative_path):
    """Execute repository source, retaining genuine public module identities."""
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, module)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(params=[4, 5], ids=["pi4", "pi5"])
def public_api(monkeypatch, request):
    """Use real wrappers/import helpers, stopping only at native boundaries."""
    board_flags = {
        "any_raspberry_pi": True,
        "any_raspberry_pi_4_board": request.param == 4,
        "any_raspberry_pi_5_board": request.param == 5,
    }
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.board_id = f"RASPBERRY_PI_{request.param}"
    agnostic.detector = SimpleNamespace(
        board=Flags(**board_flags), chip=Flags(BCM2XXX=True, id="BCM2XXX")
    )
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    monkeypatch.setattr(adafruit_blinka, "agnostic", agnostic, raising=False)
    backend_modules = {
        name: module
        for name, module in sys.modules.copy().items()
        if name.startswith(PREFIX)
    }
    for name in backend_modules:
        monkeypatch.delitem(sys.modules, name)
    for name in ("busio", "digitalio", "pwmio", "gpiod", NATIVE_PWM):
        monkeypatch.delitem(sys.modules, name, raising=False)

    native_imports, metadata_checks, resolutions, config_reads = [], [], [], []
    real_import, real_open = builtins.__import__, builtins.open

    def missing_native(name, *args, **kwargs):
        if name in ("gpiod", NATIVE_PWM):
            native_imports.append(name)
            raise ModuleNotFoundError(f"No module named '{name}'", name=name)
        return real_import(name, *args, **kwargs)

    def guarded_open(file, *args, **kwargs):
        path = str(file)
        assert not path.startswith(("/dev/", "/sys/", "/proc/")), path
        if path.endswith("microcontroller_imports.json"):
            config_reads.append(path)
        return real_open(file, *args, **kwargs)

    def missing_distribution(name):
        metadata_checks.append(name)
        raise platform_dependencies.importlib.metadata.PackageNotFoundError(name)

    def no_command(*_args, **_kwargs):
        pytest.fail("Annotation imports and missing backends must not run commands")

    monkeypatch.setattr(builtins, "__import__", missing_native)
    monkeypatch.setattr(builtins, "open", guarded_open)
    monkeypatch.setattr(
        platform_dependencies.importlib.metadata, "version", missing_distribution
    )
    for name in ("Popen", "run", "check_call", "check_output"):
        monkeypatch.setattr(subprocess, name, no_command)
    importing = load_module(
        monkeypatch, "adafruit_blinka.importing", "adafruit_blinka/importing.py"
    )
    real_resolve = importing.import_microcontroller

    def resolve(*args, **kwargs):
        resolutions.append((args[2:], kwargs))
        return real_resolve(*args, **kwargs)

    monkeypatch.setattr(importing, "import_microcontroller", resolve)
    busio = load_module(monkeypatch, "busio", "busio.py")
    digitalio = load_module(monkeypatch, "digitalio", "digitalio.py")
    pwmio = load_module(monkeypatch, "pwmio", "pwmio.py")
    api = SimpleNamespace(
        busio=busio,
        digitalio=digitalio,
        pwmio=pwmio,
        native_imports=native_imports,
        metadata_checks=metadata_checks,
        resolutions=resolutions,
        config_reads=config_reads,
        pin_module=PREFIX + f"bcm27{11 if request.param == 4 else 12}.pin",
    )
    yield api
    # import_module can populate package children outside load_module's patches.
    for name in tuple(sys.modules):
        if name.startswith(PREFIX) and name not in backend_modules:
            del sys.modules[name]


def test_downstream_annotation_shapes_need_no_backends(public_api):
    """Match eager BME280 protocol, BusDevice and Motor annotation shapes.

    These are small consumer examples, not copied/vendored driver modules.
    In particular, BME280's protocol imports have no exception guard.
    """
    consumer = ModuleType("annotation_consumer")
    exec(  # pylint: disable=exec-used
        """
from typing import Optional, Union
from busio import I2C, SPI
from digitalio import DigitalInOut
from pwmio import PWMOut

class I2C_Impl:
    def __init__(self, i2c: I2C, address: int) -> None: pass

class SPI_Impl:
    def __init__(self, spi: SPI, cs: DigitalInOut) -> None: pass

class SPIDevice:
    def __init__(self, spi: SPI, chip_select: Optional[DigitalInOut] = None): pass

class DCMotor:
    def __init__(self, positive: PWMOut, negative: PWMOut): pass

class StepperMotor:
    def __init__(self, pin: Union[PWMOut, DigitalInOut]): pass
""",
        consumer.__dict__,
    )
    assert (
        get_type_hints(consumer.__dict__["I2C_Impl"].__init__)["i2c"]
        is public_api.busio.I2C
    )
    assert get_type_hints(consumer.__dict__["SPI_Impl"].__init__)["cs"] is (
        public_api.digitalio.DigitalInOut
    )
    assert get_type_hints(consumer.__dict__["DCMotor"].__init__)["positive"] is (
        public_api.pwmio.PWMOut
    )
    assert public_api.digitalio.Pin is None
    assert not public_api.native_imports
    assert not public_api.metadata_checks
    assert not public_api.resolutions
    assert not public_api.config_reads


def test_missing_gpio_fails_on_use_then_retries_and_caches(public_api, monkeypatch):
    """Real backend loading reports its missing dependency only on GPIO use."""
    digitalio = public_api.digitalio
    with pytest.raises(RuntimeError, match="platform library 'gpiod'") as raised:
        digitalio.DigitalInOut(SimpleNamespace(id=17))
    assert isinstance(raised.value.__cause__, ModuleNotFoundError)
    assert raised.value.__cause__.name == "gpiod"
    assert digitalio.Pin is None
    assert public_api.native_imports == ["gpiod"]
    assert len(public_api.resolutions) == len(public_api.config_reads) == 1

    backend = ModuleType(public_api.pin_module)
    backend.Pin = RecordingPin
    monkeypatch.setitem(sys.modules, public_api.pin_module, backend)
    first = digitalio.DigitalInOut(SimpleNamespace(id=17))
    second = digitalio.DigitalInOut(SimpleNamespace(id=18))
    assert digitalio.Pin is RecordingPin
    assert first._pin.id == 17 and second._pin.id == 18
    assert len(public_api.resolutions) == len(public_api.config_reads) == 2
    first.deinit()
    second.deinit()


def test_missing_pwm_fails_only_on_construction(public_api):
    """The real Pi adapter keeps normal wrapped native-import diagnostics."""
    with pytest.raises(RuntimeError, match=NATIVE_PWM) as raised:
        public_api.pwmio.PWMOut(SimpleNamespace(id=18))
    assert isinstance(raised.value.__cause__, ModuleNotFoundError)
    assert raised.value.__cause__.name == NATIVE_PWM
    assert public_api.native_imports == [NATIVE_PWM]
    assert public_api.metadata_checks
    assert not public_api.resolutions
    assert not public_api.config_reads


class RecordingPin:
    """Implement the existing Pin interface without devices or native code."""

    IN, OUT, OPEN_DRAIN, PULL_UP, PULL_DOWN = range(5)

    def __init__(self, pin_id):
        self.id = pin_id
        self.calls = []
        self.level = 0
        self.error = None

    def init(self, **kwargs):
        self.calls.append(("init", kwargs))
        if self.error is not None:
            raise self.error

    def value(self, value=None):
        if value is not None:
            self.level = value
        return self.level

    def deinit(self):
        self.calls.append(("deinit",))
        if self.error is not None:
            raise self.error


def test_gpio_operations_and_errors_are_unchanged(public_api, monkeypatch):
    """Delayed backend selection preserves GPIO delegation and error paths."""
    backend = ModuleType(public_api.pin_module)
    backend.Pin = RecordingPin
    monkeypatch.setitem(sys.modules, public_api.pin_module, backend)
    digitalio = public_api.digitalio
    output = digitalio.DigitalInOut(SimpleNamespace(id=17))
    pin = output._pin
    assert pin.calls == [
        ("init", {"mode": RecordingPin.IN}),
        ("init", {"mode": RecordingPin.IN, "pull": None}),
    ]
    with pytest.raises(AttributeError, match="Not an output"):
        output.value = True
    output.pull = digitalio.Pull.UP
    assert pin.calls[-1] == (
        "init",
        {"mode": RecordingPin.IN, "pull": RecordingPin.PULL_UP},
    )
    output.switch_to_input(pull=digitalio.Pull.DOWN)
    assert pin.calls[-1][1]["pull"] == RecordingPin.PULL_DOWN
    output.switch_to_output(value=True, drive_mode=digitalio.DriveMode.OPEN_DRAIN)
    assert output.value is True
    assert output.direction is digitalio.Direction.OUTPUT
    assert output.drive_mode is digitalio.DriveMode.OPEN_DRAIN
    assert pin.calls[-1] == ("init", {"mode": RecordingPin.OPEN_DRAIN})
    output.value = False
    assert output.value is False
    with pytest.raises(AttributeError, match="Not an input"):
        output.pull = None
    error = OSError("GPIO operation failed")
    pin.error = error
    with pytest.raises(OSError) as raised:
        output.switch_to_input()
    assert raised.value is error
    with pytest.raises(OSError) as raised:
        output.deinit()
    assert raised.value is error
    assert output._pin is pin  # Failed cleanup remains retryable.
    pin.error = None
    output.deinit()
    calls = list(pin.calls)
    output.deinit()
    assert output._pin is None and pin.calls == calls
