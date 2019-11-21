from adafruit_blinka.microcontroller.mcp2221.pin import Pin
from .mcp2221 import mcp2221

class I2C:

    def __init__(self, *, baudrate=100000):
        mcp2221.i2c_configure(baudrate)

    def scan(self):
        return mcp2221.i2c_scan()

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        mcp2221.i2c_writeto(address, buffer, start=start, end=end)

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
        mcp2221.i2c_readfrom_into(address, buffer, start=start, end=end)

    def writeto_then_readfrom(self, address, buffer_out, buffer_in, *,
                              out_start=0, out_end=None,
                              in_start=0, in_end=None, stop=False):
        mcp2221.i2c_writeto_then_readfrom(address, buffer_out, buffer_in,
                                          out_start=out_start, out_end=out_end,
                                          in_start=in_start, in_end=in_end)

