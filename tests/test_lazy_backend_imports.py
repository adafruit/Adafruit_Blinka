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

# Pytest supplies fixtures; assertions also inspect the wrapped pin instance.
# pylint: disable=redefined-outer-name,protected-access,too-many-locals

ROOT = Path(__file__).parents[1] / "src"
PREFIX = "adafruit_blinka.microcontroller"
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
    if "." in name:
        parent, child = name.rsplit(".", 1)
        monkeypatch.setattr(sys.modules[parent], child, module, raising=False)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(params=[4, 5], ids=["pi4", "pi5"])
def public_api(monkeypatch, request):
    """Use real wrappers/import helpers, stopping only at native boundaries."""
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.board_id = f"RASPBERRY_PI_{request.param}"
    agnostic.detector = SimpleNamespace(
        board=Flags(
            any_raspberry_pi=True,
            any_raspberry_pi_4_board=request.param == 4,
            any_raspberry_pi_5_board=request.param == 5,
        ),
        chip=Flags(BCM2XXX=True, id="BCM2XXX"),
    )
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    monkeypatch.setattr(adafruit_blinka, "agnostic", agnostic, raising=False)
    # Rebuild the whole backend package tree without mutating cached parents.
    monkeypatch.setattr(adafruit_blinka, "microcontroller", None, raising=False)
    for name in tuple(sys.modules):
        if name.startswith(PREFIX):
            monkeypatch.delitem(sys.modules, name)
    for name in ("busio", "digitalio", "pwmio", "gpiod", NATIVE_PWM):
        monkeypatch.delitem(sys.modules, name, raising=False)

    def remove_backend_imports():
        for name in tuple(sys.modules):
            if name.startswith(PREFIX):
                del sys.modules[name]

    request.addfinalizer(remove_backend_imports)
    native_imports, metadata_checks, resolutions = [], [], []
    real_import = builtins.__import__

    def missing_native(name, *args, **kwargs):
        if name in ("gpiod", NATIVE_PWM):
            native_imports.append(name)
            raise ModuleNotFoundError(f"No module named '{name}'", name=name)
        return real_import(name, *args, **kwargs)

    def missing_distribution(name):
        metadata_checks.append(name)
        raise platform_dependencies.importlib.metadata.PackageNotFoundError(name)

    def no_command(*_args, **_kwargs):
        pytest.fail("Annotation imports and missing backends must not run commands")

    monkeypatch.setattr(builtins, "__import__", missing_native)
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
    return SimpleNamespace(
        busio=load_module(monkeypatch, "busio", "busio.py"),
        digitalio=load_module(monkeypatch, "digitalio", "digitalio.py"),
        pwmio=load_module(monkeypatch, "pwmio", "pwmio.py"),
        native_imports=native_imports,
        metadata_checks=metadata_checks,
        resolutions=resolutions,
        pin_module=PREFIX + f".bcm27{11 if request.param == 4 else 12}.pin",
    )


def test_downstream_annotation_shapes_need_no_backends(public_api):
    """Small consumers mirror eager protocol, BusDevice and Motor annotations."""
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
    i2c = get_type_hints(consumer.__dict__["I2C_Impl"].__init__)
    spi = get_type_hints(consumer.__dict__["SPI_Impl"].__init__)
    motor = get_type_hints(consumer.__dict__["DCMotor"].__init__)
    assert i2c["i2c"] is public_api.busio.I2C
    assert spi["spi"] is public_api.busio.SPI
    assert spi["cs"] is public_api.digitalio.DigitalInOut
    assert motor["positive"] is public_api.pwmio.PWMOut
    assert public_api.digitalio.Pin is None
    assert not public_api.native_imports
    assert not public_api.metadata_checks
    assert not public_api.resolutions


def test_missing_gpio_fails_on_use_then_retries_and_caches(public_api, monkeypatch):
    """Real backend loading reports its missing dependency only on GPIO use."""
    digitalio = public_api.digitalio
    with pytest.raises(RuntimeError, match="platform library 'gpiod'") as raised:
        digitalio.DigitalInOut(SimpleNamespace(id=17))
    assert isinstance(raised.value.__cause__, ModuleNotFoundError)
    assert raised.value.__cause__.name == "gpiod"
    assert digitalio.Pin is None
    assert public_api.native_imports == ["gpiod"]
    assert len(public_api.resolutions) == 1

    backend = ModuleType(public_api.pin_module)
    backend.Pin = InertPin
    monkeypatch.setitem(sys.modules, public_api.pin_module, backend)
    first = digitalio.DigitalInOut(SimpleNamespace(id=17))
    second = digitalio.DigitalInOut(SimpleNamespace(id=18))
    assert digitalio.Pin is InertPin
    assert first._pin.id == 17 and second._pin.id == 18
    assert len(public_api.resolutions) == 2
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


class InertPin:
    """Only the interface needed to construct and cache a GPIO backend."""

    IN = 0

    def __init__(self, pin_id):
        self.id = pin_id

    def init(self, **_kwargs):
        """Do nothing: this test never performs a GPIO operation."""
