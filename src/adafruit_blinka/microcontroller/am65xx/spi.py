# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""am65xx SPI class using PureIO's SPI class"""

from Adafruit_PureIO import spi

# import Adafruit_PureIO.spi as spi
from adafruit_blinka.agnostic import detector


class SPI:
    """SPI Class"""

    MSB = 0
    LSB = 1
    CPHA = 1
    CPOL = 2

    baudrate = 100000
    mode = 0
    bits = 8

    def __init__(self, portid):
        if isinstance(portid, tuple):
            self._spi = spi.SPI(device=portid)
        else:
            self._spi = spi.SPI(device=(portid, 0))
        self.clock_pin = None
        self.mosi_pin = None
        self.miso_pin = None
        self.chip = None

    # pylint: disable=too-many-arguments,unused-argument
    def init(
        self,
        baudrate=100000,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=MSB,
        sck=None,
        mosi=None,
        miso=None,
    ):
        """Initialize SPI"""
        mode = 0
        if polarity:
            mode |= self.CPOL
        if phase:
            mode |= self.CPHA
        self.baudrate = baudrate
        self.mode = mode
        self.bits = bits
        self.chip = detector.chip

        # Pins are not used
        self.clock_pin = sck
        self.mosi_pin = mosi
        self.miso_pin = miso

    # pylint: enable=too-many-arguments,unused-argument

    # pylint: disable=unnecessary-pass
    def set_no_cs(self):
        """Setting so that SPI doesn't automatically set the CS pin"""
        # No kernel seems to support this, so we're just going to pass
        pass

    # pylint: enable=unnecessary-pass

    @property
    def frequency(self):
        """Return the current baudrate"""
        return self.baudrate

    def write(self, buf, start=0, end=None):
        """Write data from the buffer to SPI"""
        if not buf:
            return
        if end is None:
            end = len(buf)
        try:
            # self._spi.open(self._port, 0)
            self.set_no_cs()
            self._spi.max_speed_hz = self.baudrate
            self._spi.mode = self.mode
            self._spi.bits_per_word = self.bits
            self._spi.writebytes(buf[start:end])
            # self._spi.close()
        except FileNotFoundError:
            print("Could not open SPI device - check if SPI is enabled in kernel!")
            raise

    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read data from SPI and into the buffer"""
        if not buf:
            return
        if end is None:
            end = len(buf)
        try:
            # self._spi.open(self._port, 0)
            # self.set_no_cs()
            self._spi.max_speed_hz = self.baudrate
            self._spi.mode = self.mode
            self._spi.bits_per_word = self.bits
            data = self._spi.transfer([write_value] * (end - start))
            for i in range(end - start):  # 'readinto' the given buffer
                buf[start + i] = data[i]
            # self._spi.close()
        except FileNotFoundError:
            print("Could not open SPI device - check if SPI is enabled in kernel!")
            raise

    # pylint: disable=too-many-arguments
    def write_readinto(
        self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None
    ):
        """Perform a half-duplex write from buffer_out and then
        read data into buffer_in
        """
        if not buffer_out or not buffer_in:
            return
        if out_end is None:
            out_end = len(buffer_out)
        if in_end is None:
            in_end = len(buffer_in)
        if out_end - out_start != in_end - in_start:
            raise RuntimeError("Buffer slices must be of equal length.")
        try:
            # self._spi.open(self._port, 0)
            # self.set_no_cs()
            self._spi.max_speed_hz = self.baudrate
            self._spi.mode = self.mode
            self._spi.bits_per_word = self.bits
            data = self._spi.transfer(list(buffer_out[out_start : out_end + 1]))
            for i in range((in_end - in_start)):
                buffer_in[i + in_start] = data[i]
            # self._spi.close()
        except FileNotFoundError:
            print("Could not open SPI device - check if SPI is enabled in kernel!")
            raise

    # pylint: enable=too-many-arguments
