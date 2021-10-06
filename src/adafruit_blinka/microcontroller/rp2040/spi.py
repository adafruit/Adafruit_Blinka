"""SPI Class for RP2040"""
from machine import SPI as _SPI
from machine import Pin
from microcontroller.pin import spiPorts

# pylint: disable=protected-access, no-self-use
class SPI:
    """Custom SPI Class for RP2040"""

    MSB = _SPI.MSB

    def __init__(self, clock, MOSI=None, MISO=None, *, baudrate=1000000):
        self._frequency = baudrate
        for portId, portSck, portMosi, portMiso in spiPorts:
            if (
                (clock == portSck)
                and MOSI in (portMosi, None)  # Clock is required!
                and MISO in (portMiso, None)  # But can do with just output
            ):  # Or just input
                mosiPin = Pin(portMosi.id) if MOSI else None
                misoPin = Pin(portMiso.id) if MISO else None
                self._spi = _SPI(
                    portId,
                    sck=Pin(portSck.id),
                    mosi=mosiPin,
                    miso=misoPin,
                    baudrate=baudrate,
                )
                break
        else:
            raise ValueError(
                "No Hardware SPI on (SCLK, MOSI, MISO)={}\nValid SPI ports:{}".format(
                    (clock, MOSI, MISO), spiPorts
                )
            )

    # pylint: disable=too-many-arguments,unused-argument
    def init(
        self,
        baudrate=1000000,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=_SPI.MSB,
        sck=None,
        mosi=None,
        miso=None,
    ):
        """Initialize the Port"""
        self._frequency = baudrate
        self._spi.init(
            baudrate=baudrate,
            polarity=polarity,
            phase=phase,
            bits=bits,
            firstbit=firstbit,
        )

    # pylint: enable=too-many-arguments

    @property
    def frequency(self):
        """Return the current frequency"""
        return self._frequency

    def write(self, buf, start=0, end=None):
        """Write data from the buffer to SPI"""
        self._spi.write(buf)

    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read data from SPI and into the buffer"""
        self._spi.readinto(buf)

    # pylint: disable=too-many-arguments
    def write_readinto(
        self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None
    ):
        """Perform a half-duplex write from buffer_out and then
        read data into buffer_in
        """
        self._spi.write_readinto(
            buffer_out,
            buffer_in,
            out_start=out_start,
            out_end=out_end,
            in_start=in_start,
            in_end=in_end,
        )

    # pylint: enable=too-many-arguments
