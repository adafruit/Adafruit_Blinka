# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Generic Linux I2C class using PureIO's smbus class"""
from Adafruit_PureIO import smbus


class I2C:
    """I2C class"""

    MASTER = 0
    SLAVE = 1
    _baudrate = None
    _mode = None
    _i2c_bus = None

    # pylint: disable=unused-argument
    def __init__(self, bus_num, mode=MASTER, baudrate=None):
        if mode != self.MASTER:
            raise NotImplementedError("Only I2C Master supported!")
        _mode = self.MASTER

        # if baudrate != None:
        #    print("I2C frequency is not settable in python, ignoring!")

        try:
            self._i2c_bus = smbus.SMBus(bus_num)
        except FileNotFoundError:
            raise RuntimeError(
                "I2C Bus #%d not found, check if enabled in config!" % bus_num
            ) from RuntimeError

    # pylint: enable=unused-argument

    def scan(self):
        """Try to read a byte from each address, if you get an OSError
        it means the device isnt there"""
        found = []
        for addr in range(0, 0x80):
            try:
                self._i2c_bus.read_byte(addr)
            except OSError:
                continue
            found.append(addr)
        return found

    # pylint: disable=unused-argument
    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        """Write data from the buffer to an address"""
        if end is None:
            end = len(buffer)
        self._i2c_bus.write_bytes(address, buffer[start:end])

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
        """Read data from an address and into the buffer"""
        if end is None:
            end = len(buffer)

        readin = self._i2c_bus.read_bytes(address, end - start)
        for i in range(end - start):
            buffer[i + start] = readin[i]

    # pylint: enable=unused-argument

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
        stop=False
    ):
        """Write data from buffer_out to an address and then
        read data from an address and into buffer_in
        """
        if out_end is None:
            out_end = len(buffer_out)
        if in_end is None:
            in_end = len(buffer_in)
        if stop:
            # To generate a stop in linux, do in two transactions
            self.writeto(address, buffer_out, start=out_start, end=out_end, stop=True)
            self.readfrom_into(address, buffer_in, start=in_start, end=in_end)
        else:
            # To generate without a stop, do in one block transaction
            readin = self._i2c_bus.read_i2c_block_data(
                address, buffer_out[out_start:out_end], in_end - in_start
            )
            for i in range(in_end - in_start):
                buffer_in[i + in_start] = readin[i]
