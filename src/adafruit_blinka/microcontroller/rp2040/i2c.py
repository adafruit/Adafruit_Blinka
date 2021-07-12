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

    def writeto(self, address, buffer, *, stop=True):
        "Write data to the address from the buffer"
        return self._i2c.writeto(address, buffer, stop)

    def readfrom_into(self, address, buffer, *, stop=True):
        """Read data from an address and into the buffer"""
        return self._i2c.readfrom_into(address, buffer, stop)

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
        if out_end:
            self.writeto(address, buffer_out[out_start:out_end], stop=stop)
        else:
            self.writeto(address, buffer_out[out_start:], stop=stop)

        if not in_end:
            in_end = len(buffer_in)
        read_buffer = memoryview(buffer_in)[in_start:in_end]
        self.readfrom_into(address, read_buffer, stop=stop)
