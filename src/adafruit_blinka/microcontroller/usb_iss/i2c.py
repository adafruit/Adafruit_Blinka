# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""I2C Class for USB ISS"""
from usb_iss import UsbIss, defs


class I2C:
    """Custom I2C Class for USB ISS"""

    def __init__(self, *, frequency=400000):
        # Configure I2C mode
        self._iss = UsbIss()
        self._iss.open("/dev/ttyACM0")
        clock_khz = frequency/1000
        self._iss.setup_i2c()
        print(self._iss.i2c.read_ad0(0x40, 3))

    def scan(self):
        """Perform an I2C Device Scan"""
        raise NotImplementedError()

    # # pylint: disable=unused-argument
    # def writeto(self, address, buffer, *, start=0, end=None, stop=True):
    #     """Write data from the buffer to an address"""
    #     #self._iss.i2c.write(0x40, start, list(buffer))
    #     print ("w " + str(address))
    #     print ("ws " + str(start))
    #     self._iss.i2c.write_ad0(address, list(buffer))

    # def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
    #     """Read data from an address and into the buffer"""
    #     print ("r " + str(address))
    #     print ("s " + str(start))
    #     print ("e " + str(end))
    #     end = end if end else len(buffer)
    #     #data = self._iss.i2c.read(0x40, 0, end)
    #     data = bytes(self._iss.i2c.read_ad0(address, end))
    #     print (data)
    #     datab = bytearray(data)
    #     print (datab)
    #     print (len(datab))
    #     print (buffer)
    #     buffer[0:len(datab)] = datab
    #     print (buffer)

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        """Write data from the buffer to an address"""
        end = end if end else len(buffer)
        #port = self._i2c.get_port(address)
        #port.write(buffer[start:end], relax=stop)
        self._iss.i2c.write_ad0(address, list(buffer[start:end]))

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
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
