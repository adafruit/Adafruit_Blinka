"""I2C Class for NXP LPC4330"""
from greatfet import GreatFET


class I2C:
    """Custom I2C Class for NXP LPC4330"""

    # pylint: disable=unused-argument
    def __init__(self, *, frequency=100000):
        self._gf = GreatFET()

    def scan(self):
        """Perform an I2C Device Scan"""
        return [index for index, dev in enumerate(self._gf.i2c.scan()) if dev[0]]

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        """Write data from the buffer to an address"""
        if end is None:
            end = len(buffer)
        self._gf.i2c.write(address, buffer[start:end])

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
        """Read data from an address and into the buffer"""
        if end is None:
            end = len(buffer)
        readin = self._gf.i2c.read(address, end - start)
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
        stop=False,
    ):
        """Write data from buffer_out to an address and then
        read data from an address and into buffer_in
        """
        self.writeto(address, buffer_out, start=out_start, end=out_end, stop=stop)
        self.readfrom_into(address, buffer_in, start=in_start, end=in_end, stop=stop)
