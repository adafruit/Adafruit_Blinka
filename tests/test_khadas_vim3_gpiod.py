# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Import VIM3 pin definitions with each supported gpiod chip API."""

import importlib.util
from pathlib import Path
import sys
import types

import pytest

# Recording types preserve binding APIs without opening real GPIO controllers.
# pylint: disable=too-few-public-methods,no-self-use

SOURCE_DIRECTORY = Path(__file__).resolve().parents[1] / "src"
PACKAGE = "adafruit_blinka.microcontroller"
GENERIC = f"{PACKAGE}.generic_linux"


def load_module(monkeypatch, name):
    """Load production source without importing platform detection."""
    path = SOURCE_DIRECTORY / (name.replace(".", "/") + ".py")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, module)
    spec.loader.exec_module(module)
    return module


def load_vim3(monkeypatch, api, banks, alias="I2C3"):  # pylint: disable=too-many-locals
    """Use the real chip selector and drivers, but never acquire GPIO lines."""
    events = []

    class ChipBase:
        def __init__(self, device):
            if api == "2.x":
                if device not in ("/dev/gpiochip0", "/dev/gpiochip1"):
                    raise ValueError("gpiod 2.x requires a GPIO device path")
                self.index = int(device[-1])
            else:
                assert device in ("0", "1")
                self.index = int(device)
            events.append(("open", self.index))

    class OfficialChip(ChipBase):
        def num_lines(self):
            return banks[self.index]

        def close(self):
            events.append(("close", self.index))

    class LegacyChip(ChipBase):
        @property
        def num_lines(self):
            return banks[self.index]

        def reset(self):
            events.append(("reset", self.index))

    class ModernChip(ChipBase):
        def get_info(self):
            return types.SimpleNamespace(num_lines=banks[self.index])

        def close(self):
            events.append(("close", self.index))

    binding = types.ModuleType("gpiod")
    if api == "legacy":
        binding.chip = LegacyChip
    elif api == "1.x":
        binding.__version__ = "1.6.3"
        binding.Chip = OfficialChip
    else:
        binding.__version__ = "2.2.2"
        binding.Chip = ModernChip
    monkeypatch.setitem(sys.modules, "gpiod", binding)

    for name in (
        "adafruit_blinka",
        PACKAGE,
        GENERIC,
        f"{GENERIC}.libgpiod",
        f"{PACKAGE}.amlogic",
        f"{PACKAGE}.amlogic.a311d",
    ):
        package = types.ModuleType(name)
        package.__path__ = [str(SOURCE_DIRECTORY / name.replace(".", "/"))]
        monkeypatch.setitem(sys.modules, name, package)

    class Pin:
        def __init__(self, identifier):
            self.id = identifier

    pin_module = types.ModuleType(f"{GENERIC}.libgpiod_pin")
    pin_module.Pin = Pin
    monkeypatch.setitem(sys.modules, f"{GENERIC}.libgpiod_pin", pin_module)

    alias_module = types.ModuleType(f"{PACKAGE}.alias")

    def get_dts_alias(device):
        assert device == "ff805000.i2c"
        return alias

    alias_module.get_dts_alias = get_dts_alias
    monkeypatch.setitem(sys.modules, f"{PACKAGE}.alias", alias_module)

    for version in ("1_x", "2_x"):
        load_module(monkeypatch, f"{GENERIC}.libgpiod.libgpiod_chip_{version}")
    load_module(monkeypatch, f"{GENERIC}.libgpiod_chip")
    pins = load_module(monkeypatch, f"{PACKAGE}.amlogic.a311d.pin")
    board = load_module(monkeypatch, "adafruit_blinka.board.khadas.khadasvim3")
    return pins, board, events


@pytest.mark.parametrize("api", ("1.x", "legacy", "2.x"))
@pytest.mark.parametrize("banks", ((16, 85), (85, 16), (16, 100), (100, 16)))
def test_vim3_import_and_pin_mapping(monkeypatch, api, banks):
    """Preserve public pin maps for both bank orders and peripheral offsets."""
    pins, board, events = load_vim3(monkeypatch, api, banks)
    aobus = banks.index(16)
    periphs = 1 - aobus
    offset = banks[periphs] - 85

    assert pins.aobus == aobus
    assert pins.periphs == periphs
    assert pins.periphs_offset == offset
    assert pins.GPIOAO_0.id == (aobus, 0)
    assert pins.GPIOE_2.id == (aobus, 14)
    assert pins.GPIOZ_0.id == (periphs, offset)
    assert pins.GPIOX_19.id == (periphs, 84 + offset)
    assert board.D0 is board.GPIOAO_10 is pins.GPIO506
    assert board.D0.id == (aobus, 10)
    assert board.D9 is board.GPIOA_1 is pins.GPIO461
    assert board.D9.id == (periphs, 50 + offset)
    assert board.D16 is board.GPIOZ_15 is pins.GPIO442
    assert board.D16.id == (periphs, 15 + offset)

    assert board.SCLK is pins.SPI0_SCLK
    assert board.MCLK0 is pins.SPI0_MCLK0
    assert board.MISO is pins.SPI0_SDO
    assert board.MOSI is pins.SPI0_SDI
    assert pins.spiPorts == ((0, board.SCLK, board.MCLK0, board.MISO, board.MOSI),)
    assert board.SCLK.id == (periphs, 50 + offset)
    assert board.MCLK0.id == (periphs, 49 + offset)
    assert board.MISO.id == (periphs, 52 + offset)
    assert board.MOSI.id == (periphs, 53 + offset)
    assert board.SCL is pins.I2C3_SCL is pins.GPIOX_18
    assert board.SDA is pins.I2C3_SDA is pins.GPIOX_17
    assert board.SCL.id == (periphs, 83 + offset)
    assert board.SDA.id == (periphs, 82 + offset)
    assert pins.i2cPorts == ((3, board.SCL, board.SDA),)

    cleanup = "reset" if api == "legacy" else "close"
    assert events == [("open", 0), ("open", 1), (cleanup, 0), (cleanup, 1)]


@pytest.mark.parametrize("api", ("1.x", "legacy", "2.x"))
def test_vim3_without_i2c_alias(monkeypatch, api):
    """A missing device-tree alias does not prevent public board pin imports."""
    pins, board, _events = load_vim3(monkeypatch, api, (16, 85), alias=None)

    assert pins.i2cPorts == ()
    assert board.SCL is pins.GPIOX_18
    assert board.SDA is pins.GPIOX_17
