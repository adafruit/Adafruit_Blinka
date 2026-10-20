# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""FTDI I2C frequency forwarding without USB access or real board detection."""

import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest

import adafruit_blinka

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name

SOURCE = Path(__file__).parents[1] / "src"
MPSSE = "adafruit_blinka.microcontroller.ftdi_mpsse.mpsse"
FTDI_SOURCE = SOURCE / "adafruit_blinka/microcontroller/ftdi_mpsse"


def load_source(monkeypatch, name, path):
    """Load production code with isolated module registrations."""
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, name, module)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def ftdi(monkeypatch):
    """Use the real adapter, pin class, and URL helpers with inert PyFTDI."""
    for name in (
        "BLINKA_FT232H",
        "BLINKA_FT2232H",
        "BLINKA_FT2232H_0",
        "BLINKA_FT2232H_1",
        "BLINKA_FTX232H_0",
        "BLINKA_FTX232H_1",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setenv("BLINKA_FT2232H", "1")
    state = SimpleNamespace(controllers=[], configure_error=None)

    class RecordingController:
        """Record configuration without opening an FTDI device."""

        def __init__(self):
            self.configuration = None
            self.gpio = object()
            self.gpio_calls = 0
            state.controllers.append(self)

        def configure(self, url, **kwargs):
            """Capture exactly what is handed to PyFTDI."""
            self.configuration = (url, kwargs)
            if state.configure_error is not None:
                raise state.configure_error

        def get_gpio(self):
            """Supply an inert GPIO controller for the existing Pin handoff."""
            self.gpio_calls += 1
            return self.gpio

    package = ModuleType("pyftdi")
    package.__path__ = []
    package.i2c = ModuleType("pyftdi.i2c")
    package.i2c.I2cController = RecordingController
    monkeypatch.setitem(sys.modules, "pyftdi", package)
    monkeypatch.setitem(sys.modules, "pyftdi.i2c", package.i2c)
    pin = load_source(monkeypatch, f"{MPSSE}.pin", FTDI_SOURCE / "mpsse/pin.py")
    state.original_gpio = SimpleNamespace(all_pins=0xFFFF)
    pin.Pin.mpsse_gpio = state.original_gpio
    state.pin_type = pin.Pin
    state.adapter = load_source(
        monkeypatch, f"{MPSSE}.i2c", FTDI_SOURCE / "mpsse/i2c.py"
    )
    return state


@pytest.mark.parametrize("interface", [None, 0, 1])
@pytest.mark.parametrize(
    "kwargs, expected",
    [
        ({}, 400000),
        ({"frequency": 100000}, 100000),
        ({"frequency": 1000000}, 1000000),
        ({"baudrate": None, "frequency": 250000}, 250000),
        ({"baudrate": 100000}, 100000),
        ({"baudrate": 400000}, 400000),
        ({"baudrate": 1000000}, 1000000),
        ({"baudrate": 100000, "frequency": 1000000}, 100000),
    ],
)
def test_backend_frequency_and_baudrate_alias(ftdi, interface, kwargs, expected):
    ftdi.adapter.I2C(interface, **kwargs)
    assert len(ftdi.controllers) == 1
    controller = ftdi.controllers[0]
    expected_url = (
        "ftdi://ftdi:ft232h/1"
        if interface is None
        else f"ftdi://ftdi:ft2232h/{interface + 1}"
    )
    assert controller.configuration == (expected_url, {"frequency": expected})
    assert ftdi.pin_type.mpsse_gpio is controller.gpio
    assert controller.gpio_calls == 1


class BoardFlags:
    """Only the chosen FTDI board is detected; no real detector is invoked."""

    def __init__(self, chip):
        self.flag = f"ftdi_{chip}"

    def __getattr__(self, name):
        return name == self.flag


@pytest.mark.parametrize(
    "chip, interface",
    [("ft232h", None), ("ft2232h", 0), ("ft2232h", 1), ("ft4232h", 0), ("ft4232h", 1)],
)
@pytest.mark.parametrize("frequency", [None, 100000, 400000, 1000000])
def test_busio_frequency_reaches_selected_interface(
    ftdi, monkeypatch, chip, interface, frequency
):
    if chip != "ft2232h":
        monkeypatch.delenv("BLINKA_FT2232H")
    pin_module = load_source(
        monkeypatch, "microcontroller.pin", FTDI_SOURCE / chip / "pin.py"
    )
    controller = ModuleType("microcontroller")
    controller.__path__ = []
    controller.pin = pin_module
    monkeypatch.setitem(sys.modules, "microcontroller", controller)
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.board_id = chip.upper()
    agnostic.detector = SimpleNamespace(
        board=BoardFlags(chip), chip=SimpleNamespace(id=None)
    )
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    monkeypatch.setattr(adafruit_blinka, "agnostic", agnostic, raising=False)
    busio = load_source(monkeypatch, "_test_ftdi_busio", SOURCE / "busio.py")
    suffix = "" if interface is None else str(interface)
    scl = getattr(pin_module, f"SCL{suffix}")
    sda = getattr(pin_module, f"SDA{suffix}")
    kwargs = {} if frequency is None else {"frequency": frequency}
    busio.I2C(scl, sda, **kwargs)
    assert len(ftdi.controllers) == 1
    assert ftdi.controllers[0].configuration == (
        f"ftdi://ftdi:{chip}/{1 if interface is None else interface + 1}",
        {"frequency": 100000 if frequency is None else frequency},
    )


@pytest.mark.parametrize("interface", [None, 0, 1])
def test_custom_device_url_is_preserved(ftdi, monkeypatch, interface):
    name = "BLINKA_FT232H" if interface is None else f"BLINKA_FTX232H_{interface}"
    chip = "232h" if interface is None else "2232h"
    url = f"ftdi://ftdi:{chip}:SERIAL/{1 if interface is None else interface + 1}"
    monkeypatch.setenv(name, url)
    ftdi.adapter.I2C(interface, baudrate=100000)
    assert ftdi.controllers[0].configuration == (url, {"frequency": 100000})


@pytest.mark.parametrize("baudrate", [0, -1, "invalid"])
def test_configuration_error_propagates_without_fallback(ftdi, baudrate):
    error = ValueError("PyFTDI configuration failed")
    ftdi.configure_error = error
    with pytest.raises(ValueError) as raised:
        ftdi.adapter.I2C(0, baudrate=baudrate)
    assert raised.value is error
    assert ftdi.controllers[0].configuration[1] == {"frequency": baudrate}
    assert ftdi.controllers[0].gpio_calls == 0
    assert ftdi.pin_type.mpsse_gpio is ftdi.original_gpio


def test_unsupported_mode_does_not_create_controller(ftdi):
    with pytest.raises(NotImplementedError, match="Only I2C Master supported"):
        ftdi.adapter.I2C(0, mode=ftdi.adapter.I2C.SLAVE, baudrate=100000)
    assert not ftdi.controllers
