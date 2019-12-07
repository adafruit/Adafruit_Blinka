from .mcp2221 import mcp2221

class I2C:

    def __init__(self, *, frequency=100000):
        self._mcp2221 = mcp2221
        self._mcp2221.i2c_configure(frequency)

    def scan(self):
        return self._mcp2221.i2c_scan()

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        self._mcp2221.i2c_writeto(address, buffer, start=start, end=end)

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
        self._mcp2221.i2c_readfrom_into(address, buffer, start=start, end=end)

    def writeto_then_readfrom(self, address, buffer_out, buffer_in, *,
                              out_start=0, out_end=None,
                              in_start=0, in_end=None, stop=False):
        self._mcp2221.i2c_writeto_then_readfrom(address, buffer_out, buffer_in,
                                          out_start=out_start, out_end=out_end,
                                          in_start=in_start, in_end=in_end)
