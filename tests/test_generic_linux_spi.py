# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import sys
import types
from unittest import mock


class FakePureIOSPI:
    last_instance = None

    def __init__(self, device):
        self.device = device
        self.max_speed_hz = None
        self.mode = None
        self.bits_per_word = None
        self.transfers = []
        FakePureIOSPI.last_instance = self

    def transfer(self, data):
        self.transfers.append(data)
        return [value + 0x10 for value in data]


def make_fake_detector():
    return types.SimpleNamespace(
        chip=types.SimpleNamespace(id="test-chip"),
        board=types.SimpleNamespace(id="test-board"),
    )


fake_platformdetect = types.ModuleType("adafruit_platformdetect")
fake_platformdetect.Detector = make_fake_detector
sys.modules.setdefault("adafruit_platformdetect", fake_platformdetect)

fake_pureio = types.ModuleType("Adafruit_PureIO")
fake_pureio.spi = types.SimpleNamespace(SPI=FakePureIOSPI)
sys.modules.setdefault("Adafruit_PureIO", fake_pureio)

# pylint: disable=wrong-import-position
from adafruit_blinka.microcontroller.generic_linux import (  # noqa: E402
    spi as generic_linux_spi,
)


@mock.patch.object(generic_linux_spi.spi, "SPI", FakePureIOSPI)
def test_write_readinto_uses_exclusive_out_end():
    FakePureIOSPI.last_instance = None
    spi = generic_linux_spi.SPI((0, 0))
    spi.init(baudrate=1000000, polarity=1, phase=1, bits=8)

    buffer_out = bytearray([0x10, 0x20, 0x30, 0x40])
    buffer_in = bytearray([0x00, 0x00, 0x00, 0x00])

    spi.write_readinto(
        buffer_out, buffer_in, out_start=1, out_end=3, in_start=1, in_end=3
    )

    assert FakePureIOSPI.last_instance.transfers == [[0x20, 0x30]]
    assert buffer_in == bytearray([0x00, 0x30, 0x40, 0x00])
