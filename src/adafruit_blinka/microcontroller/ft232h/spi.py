"""SPI Class for FT232H"""
from adafruit_blinka.microcontroller.ft232h.pin import Pin

# pylint: disable=protected-access
class SPI:
    """Custom SPI Class for FT232H"""

    MSB = 0

    def __init__(self):
        # pylint: disable=import-outside-toplevel
        from pyftdi.spi import SpiController

        # pylint: enable=import-outside-toplevel

        self._spi = SpiController(cs_count=1)
        self._spi.configure("ftdi://ftdi:ft232h/1")
        self._port = self._spi.get_port(0)
        self._port.set_frequency(100000)
        self._port._cpol = 0
        self._port._cpha = 0
        # Change GPIO controller to SPI
        Pin.ft232h_gpio = self._spi.get_gpio()

    # pylint: disable=too-many-arguments,unused-argument
    def init(
        self,
        baudrate=100000,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=MSB,
        sck=None,
        mosi=None,
        miso=None,
    ):
        """Initialize the Port"""
        self._port.set_frequency(baudrate)
        # FTDI device can only support mode 0 and mode 2
        # due to the limitation of MPSSE engine.
        # This means CPHA must = 0
        self._port._cpol = polarity
        if phase != 0:
            raise ValueError("Only SPI phase 0 is supported by FT232H.")
        self._port._cpha = phase

    # pylint: enable=too-many-arguments

    @property
    def frequency(self):
        """Return the current frequency"""
        return self._port.frequency

    def write(self, buf, start=0, end=None):
        """Write data from the buffer to SPI"""
        end = end if end else len(buf)
        chunks, rest = divmod(end - start, self._spi.PAYLOAD_MAX_LENGTH)
        for i in range(chunks):
            chunk_start = start + i * self._spi.PAYLOAD_MAX_LENGTH
            chunk_end = chunk_start + self._spi.PAYLOAD_MAX_LENGTH
            self._port.write(buf[chunk_start:chunk_end])
        if rest:
            rest_start = start + chunks * self._spi.PAYLOAD_MAX_LENGTH
            self._port.write(buf[rest_start:end])

    # pylint: disable=unused-argument
    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read data from SPI and into the buffer"""
        end = end if end else len(buf)
        result = self._port.read(end - start)
        for i, b in enumerate(result):
            buf[start + i] = b

    # pylint: enable=unused-argument

    # pylint: disable=too-many-arguments
    def write_readinto(
        self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None
    ):
        """Perform a half-duplex write from buffer_out and then
        read data into buffer_in
        """
        out_end = out_end if out_end else len(buffer_out)
        in_end = in_end if in_end else len(buffer_in)
        result = self._port.exchange(
            buffer_out[out_start:out_end], in_end - in_start, duplex=True
        )
        for i, b in enumerate(result):
            buffer_in[in_start + i] = b

    # pylint: enable=too-many-arguments
