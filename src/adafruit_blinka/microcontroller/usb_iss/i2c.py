# SPDX-FileCopyrightText: 2023 Felix Rohmeier
# SPDX-License-Identifier: MIT
"""I2C Class for USB ISS"""
from usb_iss import UsbIss


class I2C:
    """Custom I2C Class for USB ISS"""

    def __init__(self, *, frequency=400000):
        # Configure I2C mode
        self._iss = UsbIss()
        self._iss.open("/dev/ttyACM0")
        clock_khz = frequency/1000
        self._iss.setup_i2c(clock_khz = clock_khz)
        print(self._iss.i2c.read_ad0(0x40, 3))

    def scan(self):
        """Perform an I2C Device Scan"""
        raise NotImplementedError()

    def writeto(self, address, buffer, *, start=0, end=None):
        """Write data from the buffer to an address"""
        end = end if end else len(buffer)
        #port = self._i2c.get_port(address)
        #port.write(buffer[start:end], relax=stop)
        self._iss.i2c.write_ad0(address, list(buffer[start:end]))

    def readfrom_into(self, address, buffer, *, start=0, end=None):
        """Read data from an address and into the buffer"""
        end = end if end else len(buffer)
        #port = self._i2c.get_port(address)
        #result = port.read(len(buffer[start:end]), relax=stop)
        result = self._iss.i2c.read_ad0(address, len(buffer[start:end]))
        for i, b in enumerate(result):
            buffer[start + i] = b

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
        self.writeto(address, buffer_out, start=out_start, end=out_end, stop=stop)
        self.readfrom_into(address, buffer_in, start=in_start, end=in_end, stop=stop)

    # pylint: enable=unused-argument
