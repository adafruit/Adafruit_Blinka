# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Pin and Enum representations without hardware or interpreter-specific repr methods."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

from adafruit_blinka import Enum

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name

SOURCE = Path(__file__).parents[1] / "src/adafruit_blinka/microcontroller"


def load_source(name, path):
    """Load an isolated backend without triggering real board detection."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(params=[True, False], ids=["machine-pin", "enum-fallback"])
def pin_modules(request, monkeypatch):
    """Supply inert namespaces and both supported superclass-loading paths."""
    machine = ModuleType("machine")

    def native_repr(_self):
        pytest.fail("fallback must not invoke native Pin printing or read GPIO state")

    if request.param:
        machine.Pin = type("NativePin", (), {"__repr__": native_repr})
    monkeypatch.setitem(sys.modules, "machine", machine)
    board = ModuleType("board")
    controller = ModuleType("microcontroller")
    controller.__path__ = []
    controller.pin = ModuleType("microcontroller.pin")
    monkeypatch.setitem(sys.modules, "board", board)
    monkeypatch.setitem(sys.modules, "microcontroller", controller)
    monkeypatch.setitem(sys.modules, "microcontroller.pin", controller.pin)
    module = load_source(
        "_test_micropython_pin", SOURCE / "generic_micropython/__init__.py"
    )
    return SimpleNamespace(
        pin_type=module.Pin, board=board, pins=controller.pin, machine=machine
    )


@pytest.mark.parametrize("pin_id", [16, "LED", (0, 16)])
def test_unaliased_pin_has_finite_repr(pin_modules, pin_id):
    """Unknown pin aliases must not recursively call their own representation."""
    pin = pin_modules.pin_type(pin_id)
    expected = f"Pin({pin_id!r})"
    assert repr(pin) == expected
    assert repr(pin) == expected
    assert repr((pin,)) == f"({expected},)"


def test_board_pin_alias_is_preserved(pin_modules):
    """The public board name still wins over a microcontroller alias."""
    pin = pin_modules.pin_type(16)
    pin_modules.board.GP16 = pin
    pin_modules.pins.GPIO16 = pin
    assert repr(pin) == "board.GP16"


def test_microcontroller_pin_alias_is_preserved(pin_modules):
    """Pins with only a microcontroller alias retain the existing path."""
    pin = pin_modules.pin_type(16)
    pin_modules.pins.GP16 = pin
    assert repr(pin) == "microcontroller.pin.GP16"


def test_unaliased_enum_has_finite_repr():
    """The shared Enum fallback has the same recursion defect as Pin."""
    value = Enum()
    assert repr(value) == "<Enum>"
    assert repr((value,)) == "(<Enum>,)"


def test_enum_member_alias_is_preserved():
    """Named enum members keep their original fully qualified representation."""
    example = type("Example", (Enum,), {})
    value = example()
    example.VALUE = value
    assert repr(value) == f"{example.__module__}.{example.__qualname__}.VALUE"


def test_unaliased_enum_subclass_has_finite_repr():
    """A subclass need not register every instance as a class member."""
    example = type("Example", (Enum,), {})
    assert repr(example()) == "<Example>"


def test_reversed_rp2040_i2c_pins_report_value_error(pin_modules):
    """Reproduce #947's error formatting without opening an I2C peripheral."""
    scl = pin_modules.pin_type(17)
    sda = pin_modules.pin_type(16)
    pin_modules.pins.i2cPorts = ((0, scl, sda),)

    def forbidden_hardware(*_args, **_kwargs):
        pytest.fail("invalid pin selection must not construct a hardware peripheral")

    pin_modules.machine.I2C = forbidden_hardware
    pin_modules.machine.Pin = forbidden_hardware
    backend = load_source("_test_rp2040_i2c", SOURCE / "rp2040/i2c.py")
    with pytest.raises(ValueError) as raised:
        backend.I2C(scl=sda, sda=scl)
    message = str(raised.value)
    assert "No Hardware I2C on (scl,sda)=(Pin(16), Pin(17))" in message
    assert "Valid I2C ports: ((0, Pin(17), Pin(16)),)" in message
