from adafruit_blinka.microcontroller.ft232h.pin import Pin

class SPI:
    MSB = 0

    def __init__(self):
        from pyftdi.spi import SpiController
        self._spi = SpiController(cs_count=1)
        self._spi.configure('ftdi:///1')
        self._port = self._spi.get_port(0)
        self._port.set_frequency(100000)
        self._port._cpol = 0
        self._port._cpha = 0
        # Change GPIO controller to SPI
        Pin.ft232h_gpio = self._spi.get_gpio()

    def init(self, baudrate=100000, polarity=0, phase=0, bits=8,
                  firstbit=MSB, sck=None, mosi=None, miso=None):
        self._port.set_frequency(baudrate)
        # FTDI device can only support mode 0 and mode 2
        # due to the limitation of MPSSE engine.
        # This means CPHA must = 0
        self._port._cpol = polarity
        if phase != 0:
            raise ValueError("Only SPI phase 0 is supported by FT232H.")
        self._port._cpha = phase

    @property
    def frequency(self):
        return self._port.frequency

    def write(self, buf, start=0, end=None):
        end = end if end else len(buf)
        chunks, rest = divmod(end - start, self._spi.PAYLOAD_MAX_LENGTH)
        for i in range(chunks):
            chunk_start = start + i * self._spi.PAYLOAD_MAX_LENGTH
            chunk_end = chunk_start + self._spi.PAYLOAD_MAX_LENGTH
            self._port.write(buf[chunk_start:chunk_end])
        if rest:
            self._port.write(buf[-1*rest:])

    def readinto(self, buf, start=0, end=None, write_value=0):
        end = end if end else len(buf)
        result = self._port.read(end-start)
        for i, b in enumerate(result):
            buf[start+i] = b

    def write_readinto(self, buffer_out, buffer_in,  out_start=0, out_end=None, in_start=0, in_end=None):
        out_end = out_end if out_end else len(buffer_out)
        in_end = in_end if in_end else len(buffer_in)
        result = self._port.exchange(buffer_out[out_start:out_end],
                                     in_end-in_start, duplex=True)
        for i, b in enumerate(result):
            buffer_in[in_start+i] = b
