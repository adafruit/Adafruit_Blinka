"""Microcontroller pins"""

from adafruit_platformdetect.constants import chips as ap_chip
from adafruit_blinka import Enum
from adafruit_blinka.agnostic import board_id, chip_id


class Pin(Enum):
    """Reference Pin object"""

    def __init__(self, pin_id):
        """Identifier for pin, referencing platform-specific pin id"""
        self._id = pin_id

    def __repr__(self):
        # pylint: disable=import-outside-toplevel
        import board

        for key in dir(board):
            if getattr(board, key) is self:
                return "board.{}".format(key)
        import microcontroller.pin as pin

        # pylint: enable=import-outside-toplevel

        for key in dir(pin):
            if getattr(pin, key) is self:
                return "microcontroller.pin.{}".format(key)
        return repr(self)


# We intentionally are patching into this namespace so skip the wildcard check.
# pylint: disable=unused-wildcard-import,wildcard-import,ungrouped-imports

if chip_id == ap_chip.ESP8266:
    from adafruit_blinka.microcontroller.esp8266 import *
elif chip_id == ap_chip.STM32F405:
    from adafruit_blinka.microcontroller.stm32.stm32f405 import *
elif chip_id == ap_chip.BCM2XXX:
    from adafruit_blinka.microcontroller.bcm283x import *
elif chip_id == ap_chip.AM33XX:
    from adafruit_blinka.microcontroller.am335x import *
elif chip_id == ap_chip.SUN8I:
    from adafruit_blinka.microcontroller.allwinner.h3 import *
elif chip_id == ap_chip.SAMA5:
    from adafruit_blinka.microcontroller.sama5 import *
elif chip_id == ap_chip.T210:
    from adafruit_blinka.microcontroller.tegra.t210 import *
elif chip_id == ap_chip.T186:
    from adafruit_blinka.microcontroller.tegra.t186 import *
elif chip_id == ap_chip.T194:
    from adafruit_blinka.microcontroller.tegra.t194 import *
elif chip_id == ap_chip.S905:
    from adafruit_blinka.microcontroller.amlogic.s905.pin import *
elif chip_id == ap_chip.S905X3:
    from adafruit_blinka.microcontroller.amlogic.s905x3.pin import *
elif chip_id == ap_chip.S922X:
    from adafruit_blinka.microcontroller.amlogic.s922x.pin import *
elif chip_id == ap_chip.EXYNOS5422:
    from adafruit_blinka.microcontroller.samsung.exynos5422.pin import *
elif chip_id == ap_chip.APQ8016:
    from adafruit_blinka.microcontroller.snapdragon.apq8016.pin import *
elif chip_id == ap_chip.A64:
    from adafruit_blinka.microcontroller.allwinner.a64.pin import *
elif chip_id == ap_chip.A33:
    from adafruit_blinka.microcontroller.allwinner.a33.pin import *
elif chip_id == ap_chip.RK3308:
    from adafruit_blinka.microcontroller.rockchip.rk3308.pin import *
elif chip_id == ap_chip.IMX8MX:
    from adafruit_blinka.microcontroller.nxp_imx8m import *
elif chip_id == ap_chip.HFU540:
    from adafruit_blinka.microcontroller.hfu540.pin import *
elif chip_id == ap_chip.BINHO:
    from adafruit_blinka.microcontroller.nova import *
elif chip_id == ap_chip.LPC4330:
    from adafruit_blinka.microcontroller.nxp_lpc4330 import *
elif chip_id == ap_chip.MIPS24KC:
    from adafruit_blinka.microcontroller.atheros.ar9331.pin import *
elif chip_id == ap_chip.MIPS24KEC:
    from adafruit_blinka.microcontroller.mips24kec.pin import *
elif chip_id == ap_chip.PENTIUM_N3710:
    from adafruit_blinka.microcontroller.pentium.n3710.pin import *
elif chip_id == ap_chip.STM32MP157:
    from adafruit_blinka.microcontroller.stm32.stm32mp157.pin import *
else:
    raise NotImplementedError("Microcontroller not supported:", chip_id)
