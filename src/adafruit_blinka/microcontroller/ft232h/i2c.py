from adafruit_blinka.microcontroller.ft232h.pin import Pin

class I2C:

    def __init__(self, *, frequency=400000):
        # change GPIO controller to I2C
        from pyftdi.i2c import I2cController
        self._i2c = I2cController()
        self._i2c.configure('ftdi://ftdi:ft232h/1', frequency=frequency)
        Pin.ft232h_gpio = self._i2c.get_gpio()

    def scan(self):
        return [addr for addr in range(0x79) if self._i2c.poll(addr)]

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        end = end if end else len(buffer)
        port = self._i2c.get_port(address)
        port.write(buffer[start:end], relax=stop)

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
        end = end if end else len(buffer)
        port = self._i2c.get_port(address)
        result = port.read(len(buffer[start:end]), relax=stop)
        for i, b in enumerate(result):
            buffer[start+i] = b

    def writeto_then_readfrom(self, address, buffer_out, buffer_in, *,
                              out_start=0, out_end=None,
                              in_start=0, in_end=None, stop=False):
        out_end = out_end if out_end else len(buffer_out)
        in_end = in_end if in_end else len(buffer_in)
        port = self._i2c.get_port(address)
        result = port.exchange(buffer_out[out_start:out_end],
                               in_end-in_start,
                               relax=True)
        for i, b in enumerate(result):
            buffer_in[in_start+i] = b
