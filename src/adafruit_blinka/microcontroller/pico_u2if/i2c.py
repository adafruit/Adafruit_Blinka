"""I2C Class for Pico u2if"""
from .pico_u2if import pico_u2if


class I2C:
    """Custom I2C Class for Pico u2if"""

    def __init__(self, scl, sda, *, frequency=100000):
        index = None
        if scl.id == 5 and sda.id == 4:
            index = 0
        if scl.id == 15 and sda.id == 14:
            index = 1
        if index is None:
            raise ValueError("I2C not found on specified pins.")
        self._index = index
        pico_u2if.i2c_set_port(self._index)
        pico_u2if.i2c_configure(frequency)

    def scan(self):
        """Perform an I2C Device Scan"""
        pico_u2if.i2c_set_port(self._index)
        return pico_u2if.i2c_scan()

    # pylint: disable=unused-argument
    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        """Write data from the buffer to an address"""
        pico_u2if.i2c_set_port(self._index)
        pico_u2if.i2c_writeto(address, buffer, start=start, end=end)

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
        """Read data from an address and into the buffer"""
        pico_u2if.i2c_set_port(self._index)
        pico_u2if.i2c_readfrom_into(address, buffer, start=start, end=end)

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
        pico_u2if.i2c_set_port(self._index)
        pico_u2if.i2c_writeto_then_readfrom(
            address,
            buffer_out,
            buffer_in,
            out_start=out_start,
            out_end=out_end,
            in_start=in_start,
            in_end=in_end,
        )

    # pylint: enable=unused-argument
