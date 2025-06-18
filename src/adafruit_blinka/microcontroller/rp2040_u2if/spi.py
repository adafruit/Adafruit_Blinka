# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""SPI Classes for RP2040s with u2if firmware"""
from .rp2040_u2if import rp2040_u2if


# pylint: disable=protected-access, no-self-use
class SPI:
    """SPI Base Class for RP2040 u2if"""

    MSB = 0

    def __init__(self, index, *, baudrate=100000):
        self._index = index
        self._frequency = baudrate
        rp2040_u2if.spi_set_port(self._index)
        rp2040_u2if.spi_configure(self._frequency)

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
        rp2040_u2if.spi_set_port(self._index)
        rp2040_u2if.spi_configure(self._frequency)

    # pylint: enable=too-many-arguments

    @property
    def frequency(self):
        """Return the current frequency"""
        return self._frequency

    def write(self, buf, start=0, end=None):
        """Write data from the buffer to SPI"""
        rp2040_u2if.spi_write(buf, start=start, end=end)

    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read data from SPI and into the buffer"""
        rp2040_u2if.spi_readinto(buf, start=start, end=end, write_value=write_value)

    # pylint: disable=too-many-arguments
    def write_readinto(
        self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None
    ):
        """Perform a half-duplex write from buffer_out and then
        read data into buffer_in
        """
        rp2040_u2if.spi_write_readinto(
            buffer_out,
            buffer_in,
            out_start=out_start,
            out_end=out_end,
            in_start=in_start,
            in_end=in_end,
        )

    # pylint: enable=too-many-arguments


class SPI_Pico(SPI):
    """SPI Class for Pico u2if"""

    def __init__(self, clock, *, baudrate=100000):
        index = None
        if clock.id == 18:
            index = 0
        if clock.id == 10:
            index = 1
        if index is None:
            raise ValueError("No SPI port on specified pin.")
        super().__init__(index, baudrate=baudrate)


class SPI_Feather(SPI):
    """SPI Class for Feather u2if"""

    def __init__(self, clock, *, baudrate=100000):
        index = None
        if clock.id == 18:
            index = 0
        if index is None:
            raise ValueError("No SPI port on specified pin.")
        super().__init__(index, baudrate=baudrate)


class SPI_Feather_CAN(SPI):
    """SPI Class for Feather EPD u2if"""

    def __init__(self, clock, *, baudrate=100000):
        index = None
        if clock.id == 14:
            index = 1
        if index is None:
            raise ValueError("No SPI port on specified pin.")
        super().__init__(index, baudrate=baudrate)


class SPI_Feather_EPD(SPI):
    """SPI Class for Feather EPD u2if"""

    def __init__(self, clock, *, baudrate=100000):
        index = None
        if clock.id == 22:
            index = 0
        if clock.id == 14:
            index = 1
        if index is None:
            raise ValueError("No SPI port on specified pin.")
        super().__init__(index, baudrate=baudrate)


class SPI_Feather_RFM(SPI):
    """SPI Class for Feather EPD u2if"""

    def __init__(self, clock, *, baudrate=100000):
        index = None
        if clock.id == 14:
            index = 1
        if index is None:
            raise ValueError("No SPI port on specified pin.")
        super().__init__(index, baudrate=baudrate)


class SPI_QTPY(SPI):
    """SPI Class for QT Py u2if"""

    def __init__(self, clock, *, baudrate=100000):
        index = None
        if clock.id == 6:
            index = 0
        if index is None:
            raise ValueError("No SPI port on specified pin.")
        super().__init__(index, baudrate=baudrate)


class SPI_ItsyBitsy(SPI):
    """SPI Class for ItsyBitsy u2if"""

    def __init__(self, clock, *, baudrate=100000):
        index = None
        if clock.id == 18:
            index = 0
        if index is None:
            raise ValueError("No SPI port on specified pin.")
        super().__init__(index, baudrate=baudrate)


class SPI_MacroPad(SPI):
    """SPI Class for MacroPad u2if"""

    def __init__(self, clock, *, baudrate=100000):
        index = None
        if clock.id == 26:
            index = 1
        if index is None:
            raise ValueError("No SPI port on specified pin.")
        super().__init__(index, baudrate=baudrate)


class SPI_KB2040(SPI):
    """SPI Class for KB2040 u2if"""

    def __init__(self, clock, *, baudrate=100000):
        index = None
        if clock.id == 18:
            index = 0
        if index is None:
            raise ValueError("No SPI port on specified pin.")
        super().__init__(index, baudrate=baudrate)


class SPI_Radxa_X4(SPI):
    """SPI Class for Radxa X4 u2if"""

    def __init__(self, clock, *, baudrate=100000):
        index = None
        if clock.id == 6:
            index = 0
        if clock.id == 10:
            index = 1
        if index is None:
            raise ValueError("No SPI port on specified pin.")
        super().__init__(index, baudrate=baudrate)
