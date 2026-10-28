# SPDX-FileCopyrightText: 2026 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""MCP2222 SPI transfers, pin reservation, and public busio routing."""

import importlib.util
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from pymcp2222.exceptions import SPIError
from pymcp2222.spi import SPIMode, SPISpeed


@pytest.fixture(name="backend")
def mcp2222_spi_backend(monkeypatch):
    device = SimpleNamespace(spi=Mock(), io=Mock())
    package = "adafruit_blinka.microcontroller.mcp2222"
    monkeypatch.setitem(
        sys.modules, package + ".mcp2222", SimpleNamespace(mcp2222=device)
    )
    modules = []
    for name in ("pin", "spi"):
        path = Path(__file__).parents[1] / "src" / Path(*package.split("."))
        spec = importlib.util.spec_from_file_location(
            package + "." + name, path / (name + ".py")
        )
        module = importlib.util.module_from_spec(spec)
        monkeypatch.setitem(sys.modules, spec.name, module)
        spec.loader.exec_module(module)
        modules.append(module)
    pin, spi_module = modules[0], modules[1]
    spi = spi_module.SPI()
    yield device, spi, pin
    spi.deinit()


@pytest.mark.parametrize("polarity,phase", [(0, 0), (0, 1), (1, 0), (1, 1)])
def test_modes_and_frequency_rounding(backend, polarity, phase):
    device, spi, _ = backend
    spi.init(baudrate=1000000, polarity=polarity, phase=phase)
    params = device.spi.configure.call_args.args[0]
    assert params.mode == SPIMode(0x44 + 2 * polarity + phase)
    assert params.speed == SPISpeed.FREQ_750KHZ
    assert spi.frequency == 750000
    spi.init(baudrate=100000)
    assert spi.frequency == 187500
    spi.init(baudrate=20000000)
    assert spi.frequency == 12000000


@pytest.mark.parametrize(
    "settings",
    [{"baudrate": 0}, {"polarity": 2}, {"phase": 2}, {"bits": 16}, {"firstbit": 1}],
)
def test_invalid_configuration_does_not_touch_hardware(backend, settings):
    device, spi, _ = backend
    device.spi.reset_mock()
    with pytest.raises(ValueError):
        spi.init(**settings)
    device.spi.configure.assert_not_called()


def test_slices_fill_byte_and_overlapping_buffers(backend):
    device, spi, _ = backend
    spi.write(b"abcdef", 1, 4)
    device.spi.write.assert_called_once_with(b"bcd")
    device.spi.exchange.side_effect = lambda data: data
    buffer = bytearray(b"abcdef")
    spi.write_readinto(buffer, buffer, 0, 3, 2, 5)
    assert buffer == b"ababcf"
    spi.readinto(buffer, 1, 4, write_value=0xA5)
    assert buffer == b"a\xa5\xa5\xa5cf"
    device.spi.exchange.assert_called_with(b"\xa5\xa5\xa5")


def test_empty_and_invalid_buffers(backend):
    device, spi, _ = backend
    spi.write(b"abc", end=0)
    spi.readinto(bytearray(), write_value=255)
    spi.write_readinto(b"", bytearray())
    with pytest.raises(ValueError, match="same length"):
        spi.write_readinto(b"ab", bytearray(1))
    with pytest.raises(TypeError, match="writable"):
        spi.write_readinto(b"ab", b"cd")
    with pytest.raises(ValueError):
        spi.readinto(bytearray(1), write_value=256)
    device.spi.write.assert_not_called()
    device.spi.exchange.assert_not_called()


def test_transfer_errors_and_short_reads(backend):
    device, spi, _ = backend
    device.spi.write.side_effect = SPIError("USB failure")
    device.spi.exchange.side_effect = SPIError("USB failure")
    with pytest.raises(OSError, match="USB failure"):
        spi.write(b"a")
    with pytest.raises(OSError, match="USB failure"):
        spi.readinto(bytearray(1))
    device.spi.exchange.side_effect = None
    device.spi.exchange.return_value = b""
    with pytest.raises(OSError, match="Incomplete"):
        spi.readinto(bytearray(1))


def test_pin_reservation_and_release(backend):
    device, spi, pin = backend
    with pytest.raises(RuntimeError, match="already in use"):
        type(spi)()
    gpio = pin.Pin(4)
    with pytest.raises(RuntimeError, match="reserved"):
        gpio.init()
    with pytest.raises(RuntimeError, match="reserved"):
        gpio.value(1)
    pin.Pin(0).init()
    spi.deinit()
    device.io.set_config.assert_called_with(4, device.io.get_config.return_value)
    gpio.init()
    with pytest.raises(RuntimeError, match="deinitialized"):
        spi.write(b"a")
    spi.deinit()


def test_failed_initialization_restores_pin(backend):
    device, spi, pin = backend
    spi.deinit()
    device.spi.configure.side_effect = SPIError("configure failed")
    with pytest.raises(OSError, match="configure failed"):
        type(spi)()
    assert not pin.Pin.spi_active
    device.io.set_config.assert_called_with(4, device.io.get_config.return_value)


def test_public_busio_routes_and_releases_spi(backend, monkeypatch):
    device, spi, pin = backend
    spi.deinit()
    agnostic = SimpleNamespace(board_id="MICROCHIP_MCP2222", detector=SimpleNamespace())
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    path = Path(__file__).parents[1] / "src/busio.py"
    spec = importlib.util.spec_from_file_location("_test_mcp2222_busio", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with pytest.raises(ValueError, match="dedicated"):
        module.SPI(pin.G0, pin.MOSI, pin.MISO)
    with module.SPI(pin.SCK, pin.MOSI, pin.MISO) as public:
        with pytest.raises(RuntimeError, match="try_lock"):
            public.configure()
        assert public.try_lock()
        public.configure(baudrate=3000000, polarity=1, phase=1)
        assert public.frequency == 3000000
        device.spi.exchange.return_value = b"ab"
        buffer = bytearray(2)
        public.write_readinto(b"ab", buffer)
        assert buffer == b"ab"
        public.unlock()
    assert not pin.Pin.spi_active
