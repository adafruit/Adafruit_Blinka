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

import adafruit_platformdetect.constants.boards as ap_board
import adafruit_platformdetect.constants.chips as ap_chip
from adafruit_blinka import Enum, Lockable, agnostic
from adafruit_blinka.agnostic import board_id, detector

# pylint: disable=import-outside-toplevel,too-many-branches,too-many-statements
# pylint: disable=too-many-arguments,too-many-function-args


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
            from adafruit_blinka.microcontroller.ft232h.i2c import I2C as _I2C

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
        if detector.board.any_embedded_linux:
            from adafruit_blinka.microcontroller.generic_linux.i2c import I2C as _I2C
        else:
            from machine import I2C as _I2C
        from microcontroller.pin import i2cPorts

        for portId, portScl, portSda in i2cPorts:
            try:
                if scl == portScl and sda == portSda:
                    self._i2c = _I2C(portId, mode=_I2C.MASTER, baudrate=frequency)
                    break
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
        stop=False
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
            from adafruit_blinka.microcontroller.ft232h.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.ft232h.pin import SCK, MOSI, MISO

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
        if detector.board.any_embedded_linux:
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        else:
            from machine import SPI as _SPI
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
        if detector.board.any_raspberry_pi or detector.board.any_raspberry_pi_40_pin:
            from adafruit_blinka.microcontroller.bcm283x.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif detector.board.BEAGLEBONE_AI:
            from adafruit_blinka.microcontroller.dra74x.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif detector.board.any_beaglebone:
            from adafruit_blinka.microcontroller.am335x.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif detector.board.any_orange_pi and detector.chip.id == ap_chip.SUN8I:
            from adafruit_blinka.microcontroller.allwinner.h3.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif detector.board.any_nanopi and detector.chip.id == ap_chip.SUN8I:
            from adafruit_blinka.microcontroller.allwinner.h3.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif board_id == ap_board.GIANT_BOARD:
            from adafruit_blinka.microcontroller.sama5.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif board_id == ap_board.CORAL_EDGE_TPU_DEV:
            from adafruit_blinka.microcontroller.nxp_imx8m.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif board_id == ap_board.CORAL_EDGE_TPU_DEV_MINI:
            from adafruit_blinka.microcontroller.mt8167.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif board_id == ap_board.ODROID_C2:
            from adafruit_blinka.microcontroller.amlogic.s905.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif board_id == ap_board.ODROID_C4:
            from adafruit_blinka.microcontroller.amlogic.s905x3.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif board_id == ap_board.ODROID_XU4:
            from adafruit_blinka.microcontroller.samsung.exynos5422.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif board_id == ap_board.DRAGONBOARD_410C:
            from adafruit_blinka.microcontroller.snapdragon.apq8016.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif board_id == ap_board.JETSON_NANO:
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.tegra.t210.pin import Pin
        elif board_id == ap_board.JETSON_TX1:
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.tegra.t210.pin import Pin
        elif board_id == ap_board.JETSON_TX2:
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.tegra.t186.pin import Pin
        elif board_id == ap_board.JETSON_XAVIER:
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.tegra.t194.pin import Pin
        elif board_id == ap_board.JETSON_NX:
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.tegra.t194.pin import Pin
        elif detector.board.ROCK_PI_S:
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.rockchip.rk3308.pin import Pin
        elif detector.board.SIFIVE_UNLEASHED:
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.hfu540.pin import Pin
        elif detector.board.ftdi_ft232h:
            from adafruit_blinka.microcontroller.ft232h.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.ft232h.pin import Pin
        elif detector.board.binho_nova:
            from adafruit_blinka.microcontroller.nova.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.nova.pin import Pin
        elif detector.board.greatfet_one:
            from adafruit_blinka.microcontroller.nxp_lpc4330.spi import SPI as _SPI
            from adafruit_blinka.microcontroller.nxp_lpc4330.pin import Pin
        elif board_id in (
            ap_board.PINE64,
            ap_board.PINEBOOK,
            ap_board.PINEPHONE,
            ap_board.SOPINE,
        ):
            from adafruit_blinka.microcontroller.allwinner.a64.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif board_id == ap_board.CLOCKWORK_CPI3:
            from adafruit_blinka.microcontroller.allwinner.a33.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif board_id == ap_board.ONION_OMEGA2:
            from adafruit_blinka.microcontroller.mips24kec.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
        elif detector.board.any_lubancat and detector.chip.id == ap_chip.IMX6ULL:
            from adafruit_blinka.microcontroller.nxp_imx6ull.pin import Pin
            from adafruit_blinka.microcontroller.generic_linux.spi import SPI as _SPI
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
                miso=Pin(self._pins[2].id),
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
        except AttributeError:
            raise NotImplementedError(
                "Frequency attribute not implemented for this platform"
            ) from AttributeError

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
        else:
            from machine import UART as _UART

        if detector.board.binho_nova:
            from adafruit_blinka.microcontroller.nova.pin import uartPorts
        else:
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
