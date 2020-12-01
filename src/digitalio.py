"""
`digitalio` - Digital input and output control
=================================================

See `CircuitPython:digitalio` in CircuitPython for more details.

* Author(s): cefn
"""

from adafruit_blinka.agnostic import board_id, detector

# pylint: disable=ungrouped-imports,wrong-import-position

if detector.chip.BCM2XXX:
    from adafruit_blinka.microcontroller.bcm283x.pin import Pin
elif detector.chip.AM33XX:
    from adafruit_blinka.microcontroller.am335x.pin import Pin
elif detector.chip.SUN8I:
    from adafruit_blinka.microcontroller.allwinner.h3.pin import Pin
elif detector.chip.SAMA5:
    from adafruit_blinka.microcontroller.sama5.pin import Pin
elif detector.chip.T210:
    from adafruit_blinka.microcontroller.tegra.t210.pin import Pin
elif detector.chip.T186:
    from adafruit_blinka.microcontroller.tegra.t186.pin import Pin
elif detector.chip.T194:
    from adafruit_blinka.microcontroller.tegra.t194.pin import Pin
elif detector.chip.S905:
    from adafruit_blinka.microcontroller.amlogic.s905.pin import Pin
elif detector.chip.S905X3:
    from adafruit_blinka.microcontroller.amlogic.s905x3.pin import Pin
elif detector.chip.S922X:
    from adafruit_blinka.microcontroller.amlogic.s922x.pin import Pin
elif detector.chip.EXYNOS5422:
    from adafruit_blinka.microcontroller.samsung.exynos5422.pin import Pin
elif detector.chip.APQ8016:
    from adafruit_blinka.microcontroller.snapdragon.apq8016.pin import Pin
elif detector.chip.IMX8MX:
    from adafruit_blinka.microcontroller.nxp_imx8m.pin import Pin
elif detector.chip.HFU540:
    from adafruit_blinka.microcontroller.hfu540.pin import Pin
elif detector.chip.A64:
    from adafruit_blinka.microcontroller.allwinner.a64.pin import Pin
elif detector.chip.A33:
    from adafruit_blinka.microcontroller.allwinner.a33.pin import Pin
elif detector.chip.MIPS24KEC:
    from adafruit_blinka.microcontroller.mips24kec.pin import Pin
elif detector.chip.RK3308:
    from adafruit_blinka.microcontroller.rockchip.rk3308.pin import Pin
elif detector.board.ftdi_ft232h:
    from adafruit_blinka.microcontroller.ft232h.pin import Pin
elif detector.board.binho_nova:
    from adafruit_blinka.microcontroller.nova.pin import Pin
elif detector.board.greatfet_one:
    from adafruit_blinka.microcontroller.nxp_lpc4330.pin import Pin
elif detector.chip.STM32F405:
    from machine import Pin
elif detector.board.microchip_mcp2221:
    from adafruit_blinka.microcontroller.mcp2221.pin import Pin
elif detector.chip.PENTIUM_N3710:
    from adafruit_blinka.microcontroller.pentium.n3710.pin import Pin
elif detector.chip.STM32MP157:
    from adafruit_blinka.microcontroller.stm32.stm32mp157.pin import Pin

from adafruit_blinka import Enum, ContextManaged


class DriveMode(Enum):
    """Drive Mode Enumeration"""

    PUSH_PULL = None
    OPEN_DRAIN = None


DriveMode.PUSH_PULL = DriveMode()
DriveMode.OPEN_DRAIN = DriveMode()


class Direction(Enum):
    """Direction Enumeration"""

    INPUT = None
    OUTPUT = None


Direction.INPUT = Direction()
Direction.OUTPUT = Direction()


class Pull(Enum):
    """PullUp/PullDown Enumeration"""

    UP = None
    DOWN = None
    # NONE=None


Pull.UP = Pull()
Pull.DOWN = Pull()

# Pull.NONE = Pull()


class DigitalInOut(ContextManaged):
    """DigitalInOut CircuitPython compatibility implementation"""

    _pin = None

    def __init__(self, pin):
        self._pin = Pin(pin.id)
        self.direction = Direction.INPUT

    def switch_to_output(self, value=False, drive_mode=DriveMode.PUSH_PULL):
        """Switch the Digital Pin Mode to Output"""
        self.direction = Direction.OUTPUT
        self.value = value
        self.drive_mode = drive_mode

    def switch_to_input(self, pull=None):
        """Switch the Digital Pin Mode to Input"""
        self.direction = Direction.INPUT
        self.pull = pull

    def deinit(self):
        """Deinitialize the Digital Pin"""
        del self._pin

    @property
    def direction(self):
        """Get or Set the Digital Pin Direction"""
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value
        if value is Direction.OUTPUT:
            self._pin.init(mode=Pin.OUT)
            self.value = False
            self.drive_mode = DriveMode.PUSH_PULL
        elif value is Direction.INPUT:
            self._pin.init(mode=Pin.IN)
            self.pull = None
        else:
            raise AttributeError("Not a Direction")

    @property
    def value(self):
        """Get or Set the Digital Pin Value"""
        return self._pin.value() == 1

    @value.setter
    def value(self, val):
        if self.direction is Direction.OUTPUT:
            self._pin.value(1 if val else 0)
        else:
            raise AttributeError("Not an output")

    @property
    def pull(self):
        """Get or Set the Digital Pin Direction"""
        if self.direction is Direction.INPUT:
            return self.__pull
        raise AttributeError("Not an input")

    @pull.setter
    def pull(self, pul):
        if self.direction is Direction.INPUT:
            self.__pull = pul
            if pul is Pull.UP:
                self._pin.init(mode=Pin.IN, pull=Pin.PULL_UP)
            elif pul is Pull.DOWN:
                if hasattr(Pin, "PULL_DOWN"):
                    self._pin.init(mode=Pin.IN, pull=Pin.PULL_DOWN)
                else:
                    raise NotImplementedError(
                        "{} unsupported on {}".format(Pull.DOWN, board_id)
                    )
            elif pul is None:
                self._pin.init(mode=Pin.IN, pull=None)
            else:
                raise AttributeError("Not a Pull")
        else:
            raise AttributeError("Not an input")

    @property
    def drive_mode(self):
        """Get or Set the Digital Pin Drive Mode"""
        if self.direction is Direction.OUTPUT:
            return self.__drive_mode  #
        raise AttributeError("Not an output")

    @drive_mode.setter
    def drive_mode(self, mod):
        self.__drive_mode = mod
        if mod is DriveMode.OPEN_DRAIN:
            self._pin.init(mode=Pin.OPEN_DRAIN)
        elif mod is DriveMode.PUSH_PULL:
            self._pin.init(mode=Pin.OUT)
