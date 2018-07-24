"""
`busio` - Bus protocol support like I2C and SPI
=================================================

See `CircuitPython:busio` in CircuitPython for more details.

* Author(s): cefn
"""

from adafruit_blinka import Enum, Lockable, agnostic
from adafruit_blinka.agnostic import board_id

class I2C(Lockable):
    def __init__(self, scl, sda, frequency=400000):
        self.init(scl, sda, frequency)

    def init(self, scl, sda, frequency):
        self.deinit()
        if board_id == "raspi_3" or board_id == "raspi_2":
            from adafruit_blinka.microcontroller.raspi_23.i2c import I2C as _I2C
        else:
            from machine import I2C as _I2C
        from microcontroller.pin import i2cPorts
        for portId, portScl, portSda in i2cPorts:
            if scl == portScl and sda == portSda:
                self._i2c = _I2C(portId, mode=_I2C.MASTER, baudrate=frequency)
                break
        else:
            raise NotImplementedError("No Hardware I2C on (scl,sda)={}\nValid UART ports".format(
        (scl, sda), i2cPorts))

    def deinit(self):
        try:
            del self._i2c
        except AttributeError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()

    def scan(self):
        return self._i2c.scan()

    def readfrom_into(self, address, buffer, start=0, end=None):
        if start is not 0 or end is not None:
            if end is None:
                end = len(buffer)
            buffer = memoryview(buffer)[start:end]
        stop = True  # remove for efficiency later
        return self._i2c.readfrom_into(address, buffer, stop)

    def writeto(self, address, buffer, start=0, end=None, stop=True):
        if start is not 0 or end is not None:
            if end is None:
                return self._i2c.writeto(address, memoryview(buffer)[start:], stop)
            else:
                return self._i2c.writeto(address, memoryview(buffer)[start:end], stop)
        return self._i2c.writeto(address, buffer, stop)


class SPI(Lockable):
    def __init__(self, clock, MOSI=None, MISO=None):
        self.deinit()
        if board_id == "raspi_3" or board_id == "raspi_2":
            from adafruit_blinka.microcontroller.raspi_23.spi import SPI as _SPI
        else:
            from machine import SPI as _SPI
        from microcontroller.pin import spiPorts
        for portId, portSck, portMosi, portMiso in spiPorts:
            if clock == portSck and MOSI == portMosi and MISO == portMiso:
                self._spi = _SPI(portId)
                self._pins = (portSck, portMosi, portMiso)
                break
        else:
            raise NotImplementedError(
                "No Hardware SPI on (SCLK, MOSI, MISO)={}\nValid SPI ports:{}".
                format((clock, MOSI, MISO), spiPorts))

    def configure(self, baudrate=100000, polarity=0, phase=0, bits=8):
        if board_id == "raspi_3" or board_id == "raspi_2":
            from adafruit_blinka.microcontroller.raspi_23.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.raspi_23.pin import Pin
        else:
            from machine import SPI as _SPI
            from machine import Pin

        if self._locked:
            # TODO check if #init ignores MOSI=None rather than unsetting, to save _pinIds attribute
            self._spi.init(
                baudrate=baudrate,
                polarity=polarity,
                phase=phase,
                bits=bits,
                firstbit=_SPI.MSB,
                sck=Pin(self._pins[0].id),
                mosi=Pin(self._pins[1].id),
                miso=Pin(self._pins[2].id)
            )
        else:
            raise RuntimeError("First call try_lock()")

    def deinit(self):
        self._spi = None
        self._pinIds = None

    def write(self, buf):
        return self._spi.write(buf)

    def readinto(self, buf):
        return self._spi.readinto(buf)

    def write_readinto(self, buffer_out, buffer_in,  out_start=0, out_end=None, in_start=0, in_end=None):
        return self._spi.write_readinto(buffer_out, buffer_in, out_start, out_end, in_start, in_end)


class UART(Lockable):
    class Parity(Enum):
        pass

    Parity.ODD = Parity()
    Parity.EVEN = Parity()

    def __init__(self,
                 tx,
                 rx,
                 baudrate=9600,
                 bits=8,
                 parity=None,
                 stop=1,
                 timeout=1000,
                 receiver_buffer_size=64,
                 flow=None):
        from machine import UART as _UART
        from microcontroller.pin import uartPorts

        self.baudrate = baudrate

        if flow is not None:  # default 0
            raise NotImplementedError(
                "Parameter '{}' unsupported on {}".format(
                    "flow", agnostic.board))

        # translate parity flag for Micropython
        if parity is UART.Parity.ODD:
            parity = 1
        elif parity is UART.Parity.EVEN:
            parity = 0
        elif parity is None:
            pass
        else:
            raise ValueError("Invalid parity")

        # check tx and rx have hardware support
        for portId, portTx, portRx in uartPorts:  #
            if portTx == tx and portRx == rx:
                self._uart = _UART(
                    portId,
                    baudrate,
                    bits=bits,
                    parity=parity,
                    stop=stop,
                    timeout=timeout,
                    read_buf_len=receiver_buffer_size
                )
                break
        else:
            raise NotImplementedError(
                "No Hardware UART on (tx,rx)={}\nValid UART ports".format(
                    (tx, rx), uartPorts))

    def deinit(self):
        self._uart = None

    def read(self, nbytes=None):
        return self._uart.read(nbytes)

    def readinto(self, buf, nbytes=None):
        return self._uart.readinto(buf, nbytes)

    def readline(self):
        return self._uart.readline()

    def write(self, buf):
        return self._uart.write(buf)
