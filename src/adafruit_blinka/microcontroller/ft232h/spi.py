from adafruit_blinka.microcontroller.ft232h.pin import Pin

class SPI:
    MSB = 0

    baudrate = 100000
    mode = 0
    bits = 8

    def __init__(self):
        # change GPIO controller to SPI
        from pyftdi.spi import SpiController
        self._spi = SpiController(cs_count=1)
        self._spi.configure('ftdi:///1')
        Pin.ft232h_gpio = self._spi.get_gpio()

    def init(self, baudrate=100000, polarity=0, phase=0, bits=8,
                  firstbit=MSB, sck=None, mosi=None, miso=None):
        self.cs = 0
        self.freq = baudrate
        if polarity == 0 and phase == 0:
            self.mode = 0
        elif polarity == 0 and phase == 1:
            self.mode = 1
        elif polarity == 1 and phase == 0:
            raise ValueError("SPI mode 2 is not supported.")
        elif polarity == 1 and phase == 1:
            self.mode = 3
        else:
            raise ValueError("Unknown SPI mode.")

    def write(self, buf, start=0, end=None):
        end = end if end else len(buf)
        port = self._spi.get_port(self.cs, self.freq, self.mode)
        port.write(buf[start:end])

    def readinto(self, buf, start=0, end=None, write_value=0):
        end = end if end else len(buf)
        port = self._spi.get_port(self.cs, self.freq, self.mode)
        result = port.read(end-start)
        for i, b in enumerate(result):
            buf[start+i] = b

    def write_readinto(self, buffer_out, buffer_in,  out_start=0, out_end=None, in_start=0, in_end=None):
        out_end = out_end if out_end else len(buffer_out)
        in_end = in_end if in_end else len(buffer_in)
        port = self._spi.get_port(self.cs, self.freq, self.mode)
        result = port.exchange(buffer_out[out_start:out_end],
                               in_end-in_start)
        for i, b in enumerate(result):
            buffer_in[in_start+i] = b
