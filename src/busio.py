"""
`busio` - Bus protocol support like I2C and SPI
=================================================

See `CircuitPython:busio` in CircuitPython for more details.

* Author(s): cefn
"""

try:
    import threading
except ImportError:
    threading = None

# pylint: disable=unused-import
import adafruit_platformdetect.constants.boards as ap_board
import adafruit_platformdetect.constants.chips as ap_chip
from adafruit_blinka import Enum, Lockable, agnostic
from adafruit_blinka.agnostic import board_id, detector

# pylint: disable=import-outside-toplevel,too-many-branches,too-many-statements
# pylint: disable=too-many-arguments,too-many-function-args,too-many-return-statements


class I2C(Lockable):
    """
    Busio I2C Class for CircuitPython Compatibility. Used
    for both MicroPython and Linux.
    """

    def __init__(self, scl, sda, frequency=100000):
        self.init(scl, sda, frequency)

    def init(self, scl, sda, frequency):
        """Initialization"""
        self.deinit()
        if detector.board.ftdi_ft232h:
            from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.i2c import I2C as _I2C

            self._i2c = _I2C(frequency=frequency)
            return
        if detector.board.binho_nova:
            from adafruit_blinka.microcontroller.nova.i2c import I2C as _I2C

            self._i2c = _I2C(frequency=frequency)
            return
        if detector.board.microchip_mcp2221:
            from adafruit_blinka.microcontroller.mcp2221.i2c import I2C as _I2C

            self._i2c = _I2C(frequency=frequency)
            return
        if detector.board.greatfet_one:
            from adafruit_blinka.microcontroller.nxp_lpc4330.i2c import I2C as _I2C

            self._i2c = _I2C(frequency=frequency)
            return
        if detector.board.pico_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.i2c import I2C_Pico as _I2C

            self._i2c = _I2C(scl, sda, frequency=frequency)
            return
        if detector.board.feather_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.i2c import (
                I2C_Feather as _I2C,
            )

            self._i2c = _I2C(scl, sda, frequency=frequency)
            return
        if detector.board.qtpy_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.i2c import I2C_QTPY as _I2C

            self._i2c = _I2C(scl, sda, frequency=frequency)
            return
        if detector.board.itsybitsy_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.i2c import (
                I2C_ItsyBitsy as _I2C,
            )

            self._i2c = _I2C(scl, sda, frequency=frequency)
            return
        if detector.board.macropad_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.i2c import (
                I2C_MacroPad as _I2C,
            )

            self._i2c = _I2C(scl, sda, frequency=frequency)
            return
        if detector.board.qt2040_trinkey_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.i2c import (
                I2C_QT2040_Trinkey as _I2C,
            )

            self._i2c = _I2C(scl, sda, frequency=frequency)
            return
        if detector.chip.id == ap_chip.RP2040:
            from adafruit_blinka.microcontroller.rp2040.i2c import I2C as _I2C

            self._i2c = _I2C(scl, sda, frequency=frequency)
            return
        if detector.board.any_embedded_linux:
            from adafruit_blinka.microcontroller.generic_linux.i2c import I2C as _I2C
        elif detector.board.ftdi_ft2232h:
            from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.i2c import I2C as _I2C
        else:
            from adafruit_blinka.microcontroller.generic_micropython.i2c import (
                I2C as _I2C,
            )
        from microcontroller.pin import i2cPorts

        for portId, portScl, portSda in i2cPorts:
            try:
                # pylint: disable=unexpected-keyword-arg
                if scl == portScl and sda == portSda:
                    self._i2c = _I2C(portId, mode=_I2C.MASTER, baudrate=frequency)
                    break
                # pylint: enable=unexpected-keyword-arg
            except RuntimeError:
                pass
        else:
            raise ValueError(
                "No Hardware I2C on (scl,sda)={}\nValid I2C ports: {}".format(
                    (scl, sda), i2cPorts
                )
            )
        if threading is not None:
            self._lock = threading.RLock()

    def deinit(self):
        """Deinitialization"""
        try:
            del self._i2c
        except AttributeError:
            pass

    def __enter__(self):
        if threading is not None:
            self._lock.acquire()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if threading is not None:
            self._lock.release()
        self.deinit()

    def scan(self):
        """Scan for attached devices"""
        return self._i2c.scan()

    def readfrom_into(self, address, buffer, *, start=0, end=None):
        """Read from a device at specified address into a buffer"""
        if start != 0 or end is not None:
            if end is None:
                end = len(buffer)
            buffer = memoryview(buffer)[start:end]
        stop = True  # remove for efficiency later
        return self._i2c.readfrom_into(address, buffer, stop=stop)

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        """Write to a device at specified address from a buffer"""
        if isinstance(buffer, str):
            buffer = bytes([ord(x) for x in buffer])
        if start != 0 or end is not None:
            if end is None:
                return self._i2c.writeto(address, memoryview(buffer)[start:], stop=stop)
            return self._i2c.writeto(address, memoryview(buffer)[start:end], stop=stop)
        return self._i2c.writeto(address, buffer, stop=stop)

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
        """ "Write to a device at specified address from a buffer then read
        from a device at specified address into a buffer
        """
        return self._i2c.writeto_then_readfrom(
            address,
            buffer_out,
            buffer_in,
            out_start=out_start,
            out_end=out_end,
            in_start=in_start,
            in_end=in_end,
            stop=stop,
        )


class SPI(Lockable):
    """
    Busio SPI Class for CircuitPython Compatibility. Used
    for both MicroPython and Linux.
    """

    def __init__(self, clock, MOSI=None, MISO=None):
        self.deinit()
        if detector.board.ftdi_ft232h:
            from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.ftdi_mpsse.ft232h.pin import (
                SCK,
                MOSI,
                MISO,
            )

            self._spi = _SPI()
            self._pins = (SCK, MOSI, MISO)
            return
        if detector.board.binho_nova:
            from adafruit_blinka.microcontroller.nova.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.nova.pin import SCK, MOSI, MISO

            self._spi = _SPI(clock)
            self._pins = (SCK, MOSI, MISO)
            return
        if detector.board.greatfet_one:
            from adafruit_blinka.microcontroller.nxp_lpc4330.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.nxp_lpc4330.pin import SCK, MOSI, MISO

            self._spi = _SPI()
            self._pins = (SCK, MOSI, MISO)
            return
        if detector.board.pico_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import SPI_Pico as _SPI

            self._spi = _SPI(clock)  # this is really all that's needed
            self._pins = (clock, clock, clock)  # will determine MOSI/MISO from clock
            return
        if detector.board.feather_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import (
                SPI_Feather as _SPI,
            )

            self._spi = _SPI(clock)  # this is really all that's needed
            self._pins = (clock, clock, clock)  # will determine MOSI/MISO from clock
            return
        if detector.board.itsybitsy_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import (
                SPI_ItsyBitsy as _SPI,
            )

            self._spi = _SPI(clock)  # this is really all that's needed
            self._pins = (clock, clock, clock)  # will determine MOSI/MISO from clock
            return
        if detector.board.macropad_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import (
                SPI_MacroPad as _SPI,
            )

            self._spi = _SPI(clock)  # this is really all that's needed
            self._pins = (clock, clock, clock)  # will determine MOSI/MISO from clock
            return
        if detector.board.qtpy_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import SPI_QTPY as _SPI

            self._spi = _SPI(clock)  # this is really all that's needed
            self._pins = (clock, clock, clock)  # will determine MOSI/MISO from clock
            return
        if detector.chip.id == ap_chip.RP2040:
            from adafruit_blinka.microcontroller.rp2040.spi import SPI as _SPI

            self._spi = _SPI(clock, MOSI, MISO)  # Pins configured on instantiation
            self._pins = (clock, clock, clock)  # These don't matter, they're discarded
            return
        if detector.board.any_embedded_linux:
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif detector.board.ftdi_ft2232h:
            from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.spi import SPI as _SPI
        else:
            from adafruit_blinka.microcontroller.generic_micropython.spi import (
                SPI as _SPI,
            )
        from microcontroller.pin import spiPorts

        for portId, portSck, portMosi, portMiso in spiPorts:
            if (
                (clock == portSck)
                and MOSI in (portMosi, None)  # Clock is required!
                and MISO in (portMiso, None)  # But can do with just output
            ):  # Or just input
                self._spi = _SPI(portId)
                self._pins = (portSck, portMosi, portMiso)
                break
        else:
            raise ValueError(
                "No Hardware SPI on (SCLK, MOSI, MISO)={}\nValid SPI ports:{}".format(
                    (clock, MOSI, MISO), spiPorts
                )
            )

    def configure(self, baudrate=100000, polarity=0, phase=0, bits=8):
        """Update the configuration"""
        if detector.board.any_nanopi and detector.chip.id == ap_chip.SUN8I:
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif detector.board.ftdi_ft232h:
            from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.spi import (
                SPI as _SPI,
            )
        elif detector.board.ftdi_ft2232h:
            from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.spi import (
                SPI as _SPI,
            )
        elif detector.board.binho_nova:
            from adafruit_blinka.microcontroller.nova.spi import SPI as _SPI
        elif detector.board.greatfet_one:
            from adafruit_blinka.microcontroller.nxp_lpc4330.spi import SPI as _SPI
        elif detector.board.any_lubancat and detector.chip.id == ap_chip.IMX6ULL:
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif detector.board.pico_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import SPI_Pico as _SPI
        elif detector.board.feather_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import (
                SPI_Feather as _SPI,
            )
        elif detector.board.itsybitsy_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import (
                SPI_ItsyBitsy as _SPI,
            )
        elif detector.board.macropad_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import (
                SPI_MacroPad as _SPI,
            )
        elif detector.board.qtpy_u2if:
            from adafruit_blinka.microcontroller.rp2040_u2if.spi import SPI_QTPY as _SPI
        elif detector.chip.id == ap_chip.RP2040:
            from adafruit_blinka.microcontroller.rp2040.spi import SPI as _SPI
        elif detector.board.any_embedded_linux:
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        else:
            from adafruit_blinka.microcontroller.generic_micropython.spi import (
                SPI as _SPI,
            )

        if self._locked:
            # TODO check if #init ignores MOSI=None rather than unsetting, to save _pinIds attribute
            self._spi.init(
                baudrate=baudrate,
                polarity=polarity,
                phase=phase,
                bits=bits,
                firstbit=_SPI.MSB,
            )
        else:
            raise RuntimeError("First call try_lock()")

    def deinit(self):
        """Deinitialization"""
        self._spi = None
        self._pinIds = None

    @property
    def frequency(self):
        """Return the baud rate if implemented"""
        try:
            return self._spi.frequency
        except AttributeError as error:
            raise NotImplementedError(
                "Frequency attribute not implemented for this platform"
            ) from error

    def write(self, buf, start=0, end=None):
        """Write to the SPI device"""
        return self._spi.write(buf, start, end)

    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read from the SPI device into a buffer"""
        return self._spi.readinto(buf, start, end, write_value=write_value)

    def write_readinto(
        self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None
    ):
        """Write to the SPI device and read from the SPI device into a buffer"""
        return self._spi.write_readinto(
            buffer_out, buffer_in, out_start, out_end, in_start, in_end
        )


class UART(Lockable):
    """
    Busio UART Class for CircuitPython Compatibility. Used
    for MicroPython and a few other non-Linux boards.
    """

    class Parity(Enum):
        """Parity Enumeration"""

        pass  # pylint: disable=unnecessary-pass

    Parity.ODD = Parity()
    Parity.EVEN = Parity()

    def __init__(
        self,
        tx,
        rx,
        baudrate=9600,
        bits=8,
        parity=None,
        stop=1,
        timeout=1000,
        receiver_buffer_size=64,
        flow=None,
    ):
        if detector.board.any_embedded_linux:
            raise RuntimeError(
                "busio.UART not supported on this platform. Please use pyserial instead."
            )
        if detector.board.binho_nova:
            from adafruit_blinka.microcontroller.nova.uart import UART as _UART
        elif detector.board.greatfet_one:
            from adafruit_blinka.microcontroller.nxp_lpc4330.uart import UART as _UART
        elif detector.chip.id == ap_chip.RP2040:
            from adafruit_blinka.microcontroller.rp2040.uart import UART as _UART
        else:
            from machine import UART as _UART

        from microcontroller.pin import uartPorts

        self.baudrate = baudrate

        if flow is not None:  # default 0
            raise NotImplementedError(
                "Parameter '{}' unsupported on {}".format("flow", agnostic.board_id)
            )

        # translate parity flag for Micropython
        if parity is UART.Parity.ODD:
            parity = 1
        elif parity is UART.Parity.EVEN:
            parity = 0
        elif parity is None:
            pass
        else:
            raise ValueError("Invalid parity")

        if detector.chip.id == ap_chip.RP2040:
            self._uart = _UART(
                tx,
                rx,
                baudrate=baudrate,
                bits=bits,
                parity=parity,
                stop=stop,
            )
        else:
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
                        read_buf_len=receiver_buffer_size,
                    )
                    break
            else:
                raise ValueError(
                    "No Hardware UART on (tx,rx)={}\nValid UART ports: {}".format(
                        (tx, rx), uartPorts
                    )
                )

    def deinit(self):
        """Deinitialization"""
        if detector.board.binho_nova:
            self._uart.deinit()
        self._uart = None

    def read(self, nbytes=None):
        """Read from the UART"""
        return self._uart.read(nbytes)

    def readinto(self, buf, nbytes=None):
        """Read from the UART into a buffer"""
        return self._uart.readinto(buf, nbytes)

    def readline(self):
        """Read a line of characters up to a newline charater from the UART"""
        return self._uart.readline()

    def write(self, buf):
        """Write to the UART from a buffer"""
        return self._uart.write(buf)


class OneWire:
    """
    Stub class for OneWire, which is currently not implemented
    """

    def __init__(self, pin):
        raise NotImplementedError("OneWire has not been implemented")

    def deinit(self):
        """
        Deinitialize the OneWire bus and release any hardware resources for reuse.
        """
        raise NotImplementedError("OneWire has not been implemented")

    def reset(self):
        """
        Reset the OneWire bus and read presence
        """
        raise NotImplementedError("OneWire has not been implemented")

    def read_bit(self):
        """
        Read in a bit
        """
        raise NotImplementedError("OneWire has not been implemented")

    def write_bit(self, value):
        """
        Write out a bit based on value.
        """
        raise NotImplementedError("OneWire has not been implemented")
