"""I2C Class for RP2040"""
from machine import I2C as _I2C
from machine import Pin
from microcontroller.pin import i2cPorts


class I2C:
    """Custom I2C Class for RP2040"""

    def __init__(self, scl, sda, *, frequency=100000):
        for portId, portScl, portSda in i2cPorts:
            try:
                if scl == portScl and sda == portSda:
                    self._i2c = _I2C(
                        portId, sda=Pin(sda.id), scl=Pin(scl.id), freq=frequency
                    )
                    break
            except RuntimeError:
                pass
        else:
            raise ValueError(
                "No Hardware I2C on (scl,sda)={}\nValid I2C ports: {}".format(
                    (scl, sda), i2cPorts
                )
            )

    def scan(self):
        """Perform an I2C Device Scan"""
        return self._i2c.scan()

    # pylint: disable=unused-argument
    def writeto(self, address, buffer, *, stop=True):
        "Write data to the address from the buffer"
        return self._i2c.writeto(address, buffer)

    def readfrom_into(self, address, buffer, *, stop=True):
        """Read data from an address and into the buffer"""
        return self._i2c.readfrom_into(address, buffer)

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
        self._i2c.writeto_then_readfrom(
            address,
            buffer_out,
            buffer_in,
            out_start=out_start,
            out_end=out_end,
            in_start=in_start,
            in_end=in_end,
        )

    # pylint: enable=unused-argument
