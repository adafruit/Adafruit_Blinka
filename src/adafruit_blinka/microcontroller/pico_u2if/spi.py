"""SPI Class for Pico u2if"""
from .pico_u2if import pico_u2if

# pylint: disable=protected-access, no-self-use
class SPI:
    """Custom SPI Class for Pico u2if"""

    MSB = 0

    def __init__(self, clock, *, baudrate=100000):
        index = None
        if clock.id == 18:
            index = 0
        if clock.id == 10:
            index = 1
        if index is None:
            raise ValueError("No SPI port on specified pin.")
        self._index = index
        self._frequency = baudrate
        pico_u2if.spi_set_port(self._index)
        pico_u2if.spi_configure(self._frequency)

    # pylint: disable=too-many-arguments,unused-argument
    def init(
        self,
        baudrate=1000000,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=MSB,
        sck=None,
        mosi=None,
        miso=None,
    ):
        """Initialize the Port"""
        self._frequency = baudrate
        pico_u2if.spi_set_port(self._index)
        pico_u2if.spi_configure(self._frequency)

    # pylint: enable=too-many-arguments

    @property
    def frequency(self):
        """Return the current frequency"""
        return self._frequency

    def write(self, buf, start=0, end=None):
        """Write data from the buffer to SPI"""
        pico_u2if.spi_write(buf, start=start, end=end)

    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read data from SPI and into the buffer"""
        pico_u2if.spi_readinto(buf, start=start, end=end, write_value=write_value)

    # pylint: disable=too-many-arguments
    def write_readinto(
        self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None
    ):
        """Perform a half-duplex write from buffer_out and then
        read data into buffer_in
        """
        pico_u2if.spi_write_readinto(
            buffer_out,
            buffer_in,
            out_start=out_start,
            out_end=out_end,
            in_start=in_start,
            in_end=in_end,
        )

    # pylint: enable=too-many-arguments
