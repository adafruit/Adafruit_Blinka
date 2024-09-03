# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`microcontroller` - Pin references and cpu functionality
========================================================

* Author(s): Melissa LeBlanc-Williams
"""
import os
import sys
import time

from adafruit_platformdetect.constants import chips as ap_chip
from adafruit_blinka.agnostic import board_id, chip_id
from microcontroller import pin  # pylint: disable=unused-import
from microcontroller.pin import Pin  # pylint: disable=unused-import


def delay_us(delay):
    """Sleep for delay usecs."""
    time.sleep(delay / 1e6)


# We intentionally are patching into this namespace so skip the wildcard check.
# pylint: disable=unused-wildcard-import,wildcard-import,ungrouped-imports

if chip_id == ap_chip.ESP8266:
    from adafruit_blinka.microcontroller.esp8266 import *
elif chip_id == ap_chip.STM32F405:
    from adafruit_blinka.microcontroller.stm32.stm32f405 import *
elif chip_id == ap_chip.RP2040:
    from adafruit_blinka.microcontroller.rp2040 import *
elif chip_id == ap_chip.BCM2XXX:
    if board_id in [
        "RASPBERRY_PI_4B",
        "RASPBERRY_PI_400",
        "RASPBERRY_PI_CM4",
        "RASPBERRY_PI_5",
    ]:
        from adafruit_blinka.microcontroller.bcm2711 import *
    else:
        from adafruit_blinka.microcontroller.bcm283x import *
elif chip_id == ap_chip.DRA74X:
    from adafruit_blinka.microcontroller.dra74x import *
elif chip_id == ap_chip.AM33XX:
    from adafruit_blinka.microcontroller.am335x import *
elif chip_id == ap_chip.AM65XX:
    from adafruit_blinka.microcontroller.am65xx import *
elif chip_id == ap_chip.JH71X0:
    from adafruit_blinka.microcontroller.starfive.JH71x0 import *
elif chip_id == ap_chip.JH7110:
    from adafruit_blinka.microcontroller.starfive.JH7110 import *
elif chip_id == ap_chip.SUN4I:
    from adafruit_blinka.microcontroller.allwinner.a20 import *
elif chip_id == ap_chip.SUN7I:
    from adafruit_blinka.microcontroller.allwinner.a20 import *
elif chip_id == ap_chip.SUN8I:
    from adafruit_blinka.microcontroller.allwinner.h3 import *
elif chip_id == ap_chip.H5:
    from adafruit_blinka.microcontroller.allwinner.h5 import *
elif chip_id == ap_chip.H6:
    from adafruit_blinka.microcontroller.allwinner.h6 import *
elif chip_id == ap_chip.H618:
    from adafruit_blinka.microcontroller.allwinner.h618 import *
elif chip_id == ap_chip.H616:
    from adafruit_blinka.microcontroller.allwinner.h616 import *
elif chip_id == ap_chip.SAMA5:
    from adafruit_blinka.microcontroller.sama5 import *
elif chip_id == ap_chip.T210:
    from adafruit_blinka.microcontroller.tegra.t210 import *
elif chip_id == ap_chip.T186:
    from adafruit_blinka.microcontroller.tegra.t186 import *
elif chip_id == ap_chip.T194:
    from adafruit_blinka.microcontroller.tegra.t194 import *
elif chip_id == ap_chip.T234:
    from adafruit_blinka.microcontroller.tegra.t234 import *
elif chip_id == ap_chip.S905:
    from adafruit_blinka.microcontroller.amlogic.s905 import *
elif chip_id == ap_chip.S905X:
    from adafruit_blinka.microcontroller.amlogic.s905x import *
elif chip_id == ap_chip.S905X3:
    from adafruit_blinka.microcontroller.amlogic.s905x3 import *
elif chip_id == ap_chip.S905Y2:
    from adafruit_blinka.microcontroller.amlogic.s905y2 import *
elif chip_id == ap_chip.S922X:
    from adafruit_blinka.microcontroller.amlogic.s922x import *
elif chip_id == ap_chip.A311D:
    from adafruit_blinka.microcontroller.amlogic.a311d import *
elif chip_id == ap_chip.EXYNOS5422:
    from adafruit_blinka.microcontroller.samsung.exynos5422 import *
elif chip_id == ap_chip.APQ8016:
    from adafruit_blinka.microcontroller.snapdragon.apq8016 import *
elif chip_id == ap_chip.A10:
    from adafruit_blinka.microcontroller.allwinner.a20 import *
elif chip_id == ap_chip.A20:
    from adafruit_blinka.microcontroller.allwinner.a20 import *
elif chip_id == ap_chip.A64:
    from adafruit_blinka.microcontroller.allwinner.a64 import *
elif chip_id == ap_chip.A33:
    from adafruit_blinka.microcontroller.allwinner.a33 import *
elif chip_id == ap_chip.RK3308:
    from adafruit_blinka.microcontroller.rockchip.rk3308 import *
elif chip_id == ap_chip.RK3399:
    from adafruit_blinka.microcontroller.rockchip.rk3399 import *
elif chip_id == ap_chip.RK3399_T:
    from adafruit_blinka.microcontroller.rockchip.rk3399 import *
elif chip_id == ap_chip.RK3588:
    from adafruit_blinka.microcontroller.rockchip.rk3588 import *
elif chip_id == ap_chip.RK3328:
    from adafruit_blinka.microcontroller.rockchip.rk3328 import *
elif chip_id == ap_chip.RK3566:
    from adafruit_blinka.microcontroller.rockchip.rk3566 import *
elif chip_id == ap_chip.RK3568:
    from adafruit_blinka.microcontroller.rockchip.rk3568 import *
elif chip_id == ap_chip.H3:
    from adafruit_blinka.microcontroller.allwinner.h3 import *
elif chip_id == ap_chip.H5:
    from adafruit_blinka.microcontroller.allwinner.h5 import *
elif chip_id == ap_chip.IMX8MX:
    from adafruit_blinka.microcontroller.nxp_imx8m import *
elif chip_id == ap_chip.IMX6ULL:
    from adafruit_blinka.microcontroller.nxp_imx6ull import *
elif chip_id == ap_chip.HFU540:
    from adafruit_blinka.microcontroller.hfu540 import *
elif chip_id == ap_chip.BINHO:
    from adafruit_blinka.microcontroller.nova import *
elif chip_id == ap_chip.LPC4330:
    from adafruit_blinka.microcontroller.nxp_lpc4330 import *
elif chip_id == ap_chip.MCP2221:
    from adafruit_blinka.microcontroller.mcp2221 import *
elif chip_id == ap_chip.MIPS24KC:
    from adafruit_blinka.microcontroller.atheros.ar9331 import *
elif chip_id == ap_chip.MIPS24KEC:
    from adafruit_blinka.microcontroller.mips24kec import *
elif chip_id == ap_chip.FT232H:
    from adafruit_blinka.microcontroller.ftdi_mpsse.ft232h import *
elif chip_id == ap_chip.FT2232H:
    from adafruit_blinka.microcontroller.ftdi_mpsse.ft2232h import *
elif chip_id == ap_chip.PENTIUM_N3710:
    from adafruit_blinka.microcontroller.pentium.n3710 import *
elif chip_id == ap_chip.ATOM_J4105:
    from adafruit_blinka.microcontroller.pentium.j4105 import *
elif chip_id == ap_chip.STM32MP157:
    from adafruit_blinka.microcontroller.stm32.stm32mp157 import *
elif chip_id == ap_chip.MT8167:
    from adafruit_blinka.microcontroller.mt8167 import *
elif chip_id == ap_chip.RP2040_U2IF:
    from adafruit_blinka.microcontroller.rp2040_u2if import *
elif chip_id == ap_chip.D1_RISCV:
    from adafruit_blinka.microcontroller.allwinner.D1 import *
elif chip_id == ap_chip.CV1800B:
    from adafruit_blinka.microcontroller.cv1800b import *
elif chip_id == ap_chip.RV1103:
    from adafruit_blinka.microcontroller.rockchip.rv1103 import *
elif chip_id == ap_chip.RV1106:
    from adafruit_blinka.microcontroller.rockchip.rv1106 import *
elif chip_id == ap_chip.TH1520:
    from adafruit_blinka.microcontroller.thead.th1520 import *
elif chip_id == ap_chip.K1:
    from adafruit_blinka.microcontroller.spacemit.k1 import *
elif chip_id == ap_chip.GENERIC_X86:
    print("WARNING: GENERIC_X86 is not fully supported. Some features may not work.")
elif chip_id == ap_chip.OS_AGNOSTIC:
    from adafruit_blinka.microcontroller.generic_agnostic_board import *
elif chip_id is None:
    print(
        "WARNING: chip_id == None is not fully supported. Some features may not work."
    )
elif "sphinx" in sys.modules:
    pass
else:
    raise NotImplementedError("Microcontroller not supported:", chip_id)
