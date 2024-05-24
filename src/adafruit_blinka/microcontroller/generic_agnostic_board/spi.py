# SPDX-FileCopyrightText: 2024 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""SPI class for a generic agnostic board."""
# from .rp2040_u2if import rp2040_u2if


# pylint: disable=protected-access, no-self-use
class SPI:
    """SPI Base Class for a generic agnostic board."""

    MSB = 0

    def __init__(self, index, *, baudrate=100000):
        self._index = index
        self._frequency = baudrate

    # pylint: disable=too-many-arguments,unused-argument
    def init(
        self,
        baudrate=1000000,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=MSB,
        sck=None,
        mosi=None,
        miso=None,
    ):
        """Initialize the Port"""
        self._frequency = baudrate

    # pylint: enable=too-many-arguments

    @property
    def frequency(self):
        """Return the current frequency"""
        return self._frequency

    # pylint: disable=unnecessary-pass
    def write(self, buf, start=0, end=None):
        """Write data from the buffer to SPI"""
        pass

    # pylint: disable=unnecessary-pass
    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read data from SPI and into the buffer"""
        pass

    # pylint: disable=too-many-arguments, unnecessary-pass
    def write_readinto(
        self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None
    ):
        """Perform a half-duplex write from buffer_out and then
        read data into buffer_in
        """
        pass
