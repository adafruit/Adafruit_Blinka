"""Pins named after their chip name."""

from adafruit_platformdetect.constants import chips as ap_chip
from adafruit_blinka.agnostic import board_id, chip_id

# We intentionally are patching into this namespace so skip the wildcard check.
# pylint: disable=unused-wildcard-import,wildcard-import,ungrouped-imports

if chip_id == ap_chip.ESP8266:
    from adafruit_blinka.microcontroller.esp8266.pin import *
elif chip_id == ap_chip.STM32F405:
    from adafruit_blinka.microcontroller.stm32.stm32f405.pin import *
elif chip_id == ap_chip.RP2040:
    from adafruit_blinka.microcontroller.rp2040.pin import *
elif chip_id == ap_chip.BCM2XXX:
    if board_id in [
        "RASPBERRY_PI_4B",
        "RASPBERRY_PI_400",
        "RASPBERRY_PI_CM4",
    ]:
        from adafruit_blinka.microcontroller.bcm2711.pin import *
    else:
        from adafruit_blinka.microcontroller.bcm283x.pin import *
elif chip_id == ap_chip.DRA74X:
    from adafruit_blinka.microcontroller.dra74x.pin import *
elif chip_id == ap_chip.AM33XX:
    from adafruit_blinka.microcontroller.am335x.pin import *
elif chip_id == ap_chip.JH71x0:
    from adafruit_blinka.microcontroller.starfive.JH71x0.pin import *
elif chip_id == ap_chip.SUN8I:
    from adafruit_blinka.microcontroller.allwinner.h3.pin import *
elif chip_id == ap_chip.H3:
    from adafruit_blinka.microcontroller.allwinner.h3.pin import *
elif chip_id == ap_chip.H5:
    from adafruit_blinka.microcontroller.allwinner.h5.pin import *
elif chip_id == ap_chip.H6:
    from adafruit_blinka.microcontroller.allwinner.h6.pin import *
elif chip_id == ap_chip.H616:
    from adafruit_blinka.microcontroller.allwinner.h616.pin import *
elif chip_id == ap_chip.SAMA5:
    from adafruit_blinka.microcontroller.sama5.pin import *
elif chip_id == ap_chip.T210:
    from adafruit_blinka.microcontroller.tegra.t210.pin import *
elif chip_id == ap_chip.T186:
    from adafruit_blinka.microcontroller.tegra.t186.pin import *
elif chip_id == ap_chip.T194:
    from adafruit_blinka.microcontroller.tegra.t194.pin import *
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
elif chip_id == ap_chip.IMX8MX:
    from adafruit_blinka.microcontroller.nxp_imx8m.pin import *
elif chip_id == ap_chip.IMX6ULL:
    from adafruit_blinka.microcontroller.nxp_imx6ull.pin import *
elif chip_id == ap_chip.HFU540:
    from adafruit_blinka.microcontroller.hfu540.pin import *
elif chip_id == ap_chip.FT232H:
    from adafruit_blinka.microcontroller.ftdi_mpsse.ft232h.pin import *
elif chip_id == ap_chip.FT2232H:
    from adafruit_blinka.microcontroller.ftdi_mpsse.ft2232h.pin import *
elif chip_id == ap_chip.BINHO:
    from adafruit_blinka.microcontroller.nova.pin import *
elif chip_id == ap_chip.LPC4330:
    from adafruit_blinka.microcontroller.nxp_lpc4330.pin import *
elif chip_id == ap_chip.MCP2221:
    from adafruit_blinka.microcontroller.mcp2221.pin import *
elif chip_id == ap_chip.A64:
    from adafruit_blinka.microcontroller.allwinner.a64.pin import *
elif chip_id == ap_chip.A33:
    from adafruit_blinka.microcontroller.allwinner.a33.pin import *
elif chip_id == ap_chip.RK3308:
    from adafruit_blinka.microcontroller.rockchip.rk3308.pin import *
elif chip_id == ap_chip.RK3399:
    from adafruit_blinka.microcontroller.rockchip.rk3399.pin import *
elif chip_id == ap_chip.RK3328:
    from adafruit_blinka.microcontroller.rockchip.rk3328.pin import *
elif chip_id == ap_chip.MIPS24KC:
    from adafruit_blinka.microcontroller.atheros.ar9331.pin import *
elif chip_id == ap_chip.MIPS24KEC:
    from adafruit_blinka.microcontroller.mips24kec.pin import *
elif chip_id == ap_chip.PENTIUM_N3710:
    from adafruit_blinka.microcontroller.pentium.n3710.pin import *
elif chip_id == ap_chip.STM32MP157:
    from adafruit_blinka.microcontroller.stm32.stm32mp157.pin import *
elif chip_id == ap_chip.MT8167:
    from adafruit_blinka.microcontroller.mt8167.pin import *
elif chip_id == ap_chip.RP2040_U2IF:
    from adafruit_blinka.microcontroller.rp2040_u2if.pin import *
else:
    raise NotImplementedError("Microcontroller not supported: ", chip_id)
