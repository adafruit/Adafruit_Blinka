# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`bitbangio` - Bitbanged bus protocols
==============================================================

See `CircuitPython:bitbangio` in CircuitPython for more details.

* Author(s): cefn
"""

import adafruit_platformdetect.constants.boards as ap_board
from adafruit_blinka import Lockable, agnostic

# pylint: disable=import-outside-toplevel,too-many-arguments


class I2C(Lockable):
    """Bitbang/Software I2C implementation"""

    def __init__(self, scl, sda, frequency=400000):
        # TODO: This one is a bit questionable:
        if agnostic.board_id == ap_board.PYBOARD:
            raise NotImplementedError("No software I2C on {}".format(agnostic.board_id))
        if agnostic.detector.board.any_embedded_linux:
            # TODO: Attempt to load this library automatically
            raise NotImplementedError(
                "For bitbangio on Linux, please use Adafruit_CircuitPython_BitbangIO"
            )
        self.init(scl, sda, frequency)

    def init(self, scl, sda, frequency):
        """Initialization"""
        from machine import Pin
        from machine import I2C as _I2C

        self.deinit()
        id = (  # pylint: disable=redefined-builtin
            -1
        )  # force bitbanging implementation - in future
        # introspect platform if SDA/SCL matches hardware I2C
        self._i2c = _I2C(id, Pin(scl.id), Pin(sda.id), freq=frequency)

    def deinit(self):
        """Deinitialization"""
        try:
            del self._i2c
        except AttributeError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()

    def scan(self):
        """Scan for attached devices"""
        return self._i2c.scan()

    def readfrom_into(self, address, buffer, start=0, end=None):
        """Read from a device at specified address into a buffer"""
        if start != 0 or end is not None:
            if end is None:
                end = len(buffer)
            buffer = memoryview(buffer)[start:end]
        stop = True  # remove for efficiency later
        return self._i2c.readfrom_into(address, buffer, stop)

    def writeto(self, address, buffer, start=0, end=None, stop=True):
        """Write to a device at specified address from a buffer"""
        if start != 0 or end is not None:
            if end is None:
                return self._i2c.writeto(address, memoryview(buffer)[start:], stop)
            return self._i2c.writeto(address, memoryview(buffer)[start:end], stop)
        return self._i2c.writeto(address, buffer, stop)


# TODO untested, as actually busio.SPI was on
# tasklist https://github.com/adafruit/Adafruit_Micropython_Blinka/issues/2 :(
class SPI(Lockable):
    """Bitbang/Software SPI implementation"""

    def __init__(self, clock, MOSI=None, MISO=None):
        if agnostic.detector.board.any_embedded_linux:
            # TODO: Attempt to load this library automatically
            raise NotImplementedError(
                "For bitbangio on Linux, please use Adafruit_CircuitPython_BitbangIO"
            )
        from machine import SPI as _SPI

        self._spi = _SPI(-1)
        self._pins = (clock, MOSI, MISO)

    def configure(self, baudrate=100000, polarity=0, phase=0, bits=8):
        """Update the configuration"""
        from machine import Pin
        from machine import SPI as _SPI

        if self._locked:
            # TODO verify if _spi obj 'caches' sck, mosi, miso to
            # avoid storing in _attributeIds (duplicated in busio)
            # i.e. #init ignores MOSI=None rather than unsetting
            self._spi.init(
                baudrate=baudrate,
                polarity=polarity,
                phase=phase,
                bits=bits,
                firstbit=_SPI.MSB,
                sck=Pin(self._pins[0].id),
                mosi=Pin(self._pins[1].id),
                miso=Pin(self._pins[2].id),
            )
        else:
            raise RuntimeError("First call try_lock()")

    def write(self, buf):
        """Write to the SPI device"""
        return self._spi.write(buf)

    def readinto(self, buf):
        """Read from the SPI device into a buffer"""
        return self.readinto(buf)

    def write_readinto(self, buffer_out, buffer_in):
        """Write to the SPI device and read from the SPI device into a buffer"""
        return self.write_readinto(buffer_out, buffer_in)
