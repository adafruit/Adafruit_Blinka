# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""I2C Classes for RP2040s with u2if firmware"""
from .rp2040_u2if import rp2040_u2if


class I2C:
    """I2C Base Class for RP2040 u2if"""

    def __init__(self, index, *, frequency=100000):
        self._index = index
        rp2040_u2if.i2c_set_port(self._index)
        rp2040_u2if.i2c_configure(frequency)

    def scan(self):
        """Perform an I2C Device Scan"""
        rp2040_u2if.i2c_set_port(self._index)
        return rp2040_u2if.i2c_scan()

    # pylint: disable=unused-argument
    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        """Write data from the buffer to an address"""
        rp2040_u2if.i2c_set_port(self._index)
        rp2040_u2if.i2c_writeto(address, buffer, start=start, end=end)

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
        """Read data from an address and into the buffer"""
        rp2040_u2if.i2c_set_port(self._index)
        rp2040_u2if.i2c_readfrom_into(address, buffer, start=start, end=end)

    def writeto_then_readfrom(
        self,
        address,
        buffer_out,
        buffer_in,
        *,
        out_start=0,
        out_end=None,
        in_start=0,
        in_end=None,
        stop=False,
    ):
        """Write data from buffer_out to an address and then
        read data from an address and into buffer_in
        """
        rp2040_u2if.i2c_set_port(self._index)
        rp2040_u2if.i2c_writeto_then_readfrom(
            address,
            buffer_out,
            buffer_in,
            out_start=out_start,
            out_end=out_end,
            in_start=in_start,
            in_end=in_end,
        )

    # pylint: enable=unused-argument


class I2C_Pico(I2C):
    """I2C Class for Pico u2if"""

    def __init__(self, scl, sda, *, frequency=100000):
        index = None
        if scl.id == 5 and sda.id == 4:
            index = 0
        if scl.id == 15 and sda.id == 14:
            index = 1
        if index is None:
            raise ValueError("I2C not found on specified pins.")
        self._index = index

        super().__init__(index, frequency=frequency)


class I2C_Feather(I2C):
    """I2C Class for Feather u2if"""

    def __init__(self, scl, sda, *, frequency=100000):
        index = None
        if scl.id == 3 and sda.id == 2:
            index = 1
        if index is None:
            raise ValueError("I2C not found on specified pins.")
        self._index = index

        super().__init__(index, frequency=frequency)


class I2C_Feather_CAN(I2C):
    """I2C Class for Feather EPD u2if"""

    def __init__(self, scl, sda, *, frequency=100000):
        index = None
        if scl.id == 3 and sda.id == 2:
            index = 1
        if index is None:
            raise ValueError("I2C not found on specified pins.")
        self._index = index

        super().__init__(index, frequency=frequency)


class I2C_Feather_EPD(I2C):
    """I2C Class for Feather EPD u2if"""

    def __init__(self, scl, sda, *, frequency=100000):
        index = None
        if scl.id == 3 and sda.id == 2:
            index = 1
        if index is None:
            raise ValueError("I2C not found on specified pins.")
        self._index = index

        super().__init__(index, frequency=frequency)


class I2C_Feather_RFM(I2C):
    """I2C Class for Feather EPD u2if"""

    def __init__(self, scl, sda, *, frequency=100000):
        index = None
        if scl.id == 3 and sda.id == 2:
            index = 1
        if index is None:
            raise ValueError("I2C not found on specified pins.")
        self._index = index

        super().__init__(index, frequency=frequency)


class I2C_QTPY(I2C):
    """I2C Class for QT Py 2if"""

    def __init__(self, scl, sda, *, frequency=100000):
        index = None
        if scl.id == 25 and sda.id == 24:
            index = 0
        if scl.id == 23 and sda.id == 22:
            index = 1
        if index is None:
            raise ValueError("I2C not found on specified pins.")
        self._index = index

        super().__init__(index, frequency=frequency)


class I2C_ItsyBitsy(I2C):
    """I2C Class for ItsyBitsy u2if"""

    def __init__(self, scl, sda, *, frequency=100000):
        index = None
        if scl.id == 3 and sda.id == 2:
            index = 1
        if index is None:
            raise ValueError("I2C not found on specified pins.")
        self._index = index

        super().__init__(index, frequency=frequency)


class I2C_MacroPad(I2C):
    """I2C Class for MacroPad u2if"""

    def __init__(self, scl, sda, *, frequency=100000):
        index = None
        if scl.id == 21 and sda.id == 20:
            index = 0
        if index is None:
            raise ValueError("I2C not found on specified pins.")
        self._index = index
        super().__init__(index, frequency=frequency)


class I2C_QT2040_Trinkey(I2C):
    """I2C Class for QT2040 Trinkey u2if"""

    def __init__(self, scl, sda, *, frequency=100000):
        index = None
        if scl.id == 17 and sda.id == 16:
            index = 0
        if index is None:
            raise ValueError("I2C not found on specified pins.")
        self._index = index

        super().__init__(index, frequency=frequency)


class I2C_KB2040(I2C):
    """I2C Class for KB2040 u2if"""

    def __init__(self, scl, sda, *, frequency=100000):
        index = None
        if scl.id == 13 and sda.id == 12:
            index = 0
        if index is None:
            raise ValueError("I2C not found on specified pins.")
        self._index = index

        super().__init__(index, frequency=frequency)
