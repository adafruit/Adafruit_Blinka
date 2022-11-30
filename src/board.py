# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`board` - Define ids for available pins
=================================================

See `CircuitPython:board` in CircuitPython for more details.

* Author(s): cefn
"""


__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_Blinka.git"
__blinka__ = True


import sys

import adafruit_platformdetect.constants.boards as ap_board
from adafruit_blinka.agnostic import board_id, detector

# pylint: disable=wildcard-import,unused-wildcard-import,ungrouped-imports
# pylint: disable=import-outside-toplevel

if board_id == ap_board.FEATHER_HUZZAH:
    from adafruit_blinka.board.feather_huzzah import *

elif board_id == ap_board.NODEMCU:
    from adafruit_blinka.board.nodemcu import *

elif board_id == ap_board.PYBOARD:
    from adafruit_blinka.board.pyboard import *

elif board_id == ap_board.RASPBERRY_PI_PICO:
    from adafruit_blinka.board.raspberrypi.pico import *

elif (
    detector.board.RASPBERRY_PI_4B
    or detector.board.RASPBERRY_PI_CM4
    or detector.board.RASPBERRY_PI_400
):
    from adafruit_blinka.board.raspberrypi.raspi_4b import *

elif detector.board.any_raspberry_pi_40_pin:
    from adafruit_blinka.board.raspberrypi.raspi_40pin import *

elif detector.board.any_raspberry_pi_cm:
    from adafruit_blinka.board.raspberrypi.raspi_cm import *

elif detector.board.RASPBERRY_PI_B_REV1:
    from adafruit_blinka.board.raspberrypi.raspi_1b_rev1 import *

elif detector.board.RASPBERRY_PI_A or detector.board.RASPBERRY_PI_B_REV2:
    from adafruit_blinka.board.raspberrypi.raspi_1b_rev2 import *

elif board_id == ap_board.BEAGLEBONE:
    from adafruit_blinka.board.beagleboard.beaglebone_black import *

elif board_id == ap_board.BEAGLEBONE_BLACK:
    from adafruit_blinka.board.beagleboard.beaglebone_black import *

elif board_id == ap_board.BEAGLEBONE_GREEN:
    from adafruit_blinka.board.beagleboard.beaglebone_black import *

elif board_id == ap_board.BEAGLEBONE_GREEN_GATEWAY:
    from adafruit_blinka.board.beagleboard.beaglebone_black import *

elif board_id == ap_board.BEAGLEBONE_BLACK_INDUSTRIAL:
    from adafruit_blinka.board.beagleboard.beaglebone_black import *

elif board_id == ap_board.BEAGLEBONE_GREEN_WIRELESS:
    from adafruit_blinka.board.beagleboard.beaglebone_black import *

elif board_id == ap_board.BEAGLEBONE_BLACK_WIRELESS:
    from adafruit_blinka.board.beagleboard.beaglebone_black import *

elif board_id == ap_board.BEAGLEBONE_POCKETBEAGLE:
    from adafruit_blinka.board.beagleboard.beaglebone_pocketbeagle import *

elif board_id == ap_board.BEAGLEBONE_AI:
    from adafruit_blinka.board.beagleboard.beaglebone_ai import *

elif board_id == ap_board.BEAGLEV_STARLIGHT:
    from adafruit_blinka.board.beagleboard.beaglev_starlight import *

elif board_id == ap_board.ORANGE_PI_PC:
    from adafruit_blinka.board.orangepi.orangepipc import *

elif board_id == ap_board.ORANGE_PI_R1:
    from adafruit_blinka.board.orangepi.orangepir1 import *

elif board_id == ap_board.ORANGE_PI_ZERO:
    from adafruit_blinka.board.orangepi.orangepizero import *

elif board_id == ap_board.ORANGE_PI_ONE:
    from adafruit_blinka.board.orangepi.orangepipc import *

elif board_id == ap_board.ORANGE_PI_PC_PLUS:
    from adafruit_blinka.board.orangepi.orangepipc import *

elif board_id == ap_board.ORANGE_PI_LITE:
    from adafruit_blinka.board.orangepi.orangepipc import *

elif board_id == ap_board.ORANGE_PI_PLUS_2E:
    from adafruit_blinka.board.orangepi.orangepipc import *

elif board_id == ap_board.ORANGE_PI_2:
    from adafruit_blinka.board.orangepi.orangepipc import *

elif board_id == ap_board.ORANGE_PI_ZERO_PLUS_2H5:
    from adafruit_blinka.board.orangepi.orangepizeroplus2h5 import *

elif board_id == ap_board.ORANGE_PI_ZERO_PLUS:
    from adafruit_blinka.board.orangepi.orangepizeroplus import *

elif board_id == ap_board.ORANGE_PI_ZERO_2:
    from adafruit_blinka.board.orangepi.orangepizero2 import *

elif board_id == ap_board.ORANGE_PI_3:
    from adafruit_blinka.board.orangepi.orangepi3 import *

elif board_id == ap_board.ORANGE_PI_4:
    from adafruit_blinka.board.orangepi.orangepi4 import *

elif board_id == ap_board.ORANGE_PI_4_LTS:
    from adafruit_blinka.board.orangepi.orangepi4 import *

elif board_id == ap_board.BANANA_PI_M2_ZERO:
    from adafruit_blinka.board.bananapi.bpim2zero import *

elif board_id == ap_board.BANANA_PI_M2_PLUS:
    from adafruit_blinka.board.bananapi.bpim2plus import *

elif board_id == ap_board.BANANA_PI_M5:
    from adafruit_blinka.board.bananapi.bpim5 import *

elif board_id == ap_board.GIANT_BOARD:
    from adafruit_blinka.board.giantboard import *

elif board_id == ap_board.JETSON_TX1:
    from adafruit_blinka.board.nvidia.jetson_tx1 import *

elif board_id == ap_board.JETSON_TX2:
    from adafruit_blinka.board.nvidia.jetson_tx2 import *

elif board_id == ap_board.JETSON_TX2_NX:
    from adafruit_blinka.board.nvidia.jetson_tx2_nx import *

elif board_id == ap_board.JETSON_XAVIER:
    from adafruit_blinka.board.nvidia.jetson_xavier import *

elif board_id == ap_board.JETSON_NANO:
    from adafruit_blinka.board.nvidia.jetson_nano import *

elif board_id == ap_board.JETSON_NX:
    from adafruit_blinka.board.nvidia.jetson_nx import *

elif board_id == ap_board.JETSON_AGX_ORIN:
    from adafruit_blinka.board.nvidia.jetson_orin import *

elif board_id == ap_board.CLARA_AGX_XAVIER:
    from adafruit_blinka.board.nvidia.clara_agx_xavier import *

elif board_id == ap_board.CORAL_EDGE_TPU_DEV:
    from adafruit_blinka.board.coral_dev_board import *

elif board_id == ap_board.CORAL_EDGE_TPU_DEV_MINI:
    from adafruit_blinka.board.coral_dev_board_mini import *

elif board_id == ap_board.ODROID_C2:
    from adafruit_blinka.board.hardkernel.odroidc2 import *

elif board_id == ap_board.ODROID_C4:
    from adafruit_blinka.board.hardkernel.odroidc4 import *

elif board_id == ap_board.ODROID_N2:
    from adafruit_blinka.board.hardkernel.odroidn2 import *

elif board_id == ap_board.KHADAS_VIM3:
    from adafruit_blinka.board.khadas.khadasvim3 import *

elif board_id == ap_board.ODROID_XU4:
    from adafruit_blinka.board.hardkernel.odroidxu4 import *

elif board_id == ap_board.DRAGONBOARD_410C:
    from adafruit_blinka.board.dragonboard_410c import *

elif board_id == ap_board.FTDI_FT232H:
    from adafruit_blinka.board.ftdi_ft232h import *

elif board_id == ap_board.FTDI_FT2232H:
    from adafruit_blinka.board.ftdi_ft2232h import *

elif board_id == ap_board.BINHO_NOVA:
    from adafruit_blinka.board.binho_nova import *

elif board_id == ap_board.MICROCHIP_MCP2221:
    from adafruit_blinka.board.microchip_mcp2221 import *

elif board_id == ap_board.GREATFET_ONE:
    from adafruit_blinka.board.greatfet_one import *

elif board_id == ap_board.SIFIVE_UNLEASHED:
    from adafruit_blinka.board.hifive_unleashed import *

elif board_id == ap_board.PINE64:
    from adafruit_blinka.board.pine64 import *

elif board_id == ap_board.PINEH64:
    from adafruit_blinka.board.pineH64 import *

elif board_id == ap_board.SOPINE:
    from adafruit_blinka.board.soPine import *

elif board_id == ap_board.CLOCKWORK_CPI3:
    from adafruit_blinka.board.clockworkcpi3 import *

elif board_id == ap_board.ONION_OMEGA2:
    from adafruit_blinka.board.onion.omega2 import *

elif board_id == ap_board.RADXA_ZERO:
    from adafruit_blinka.board.radxa.radxazero import *

elif board_id == ap_board.ROCK_PI_S:
    from adafruit_blinka.board.radxa.rockpis import *

elif board_id == ap_board.ROCK_PI_4:
    from adafruit_blinka.board.radxa.rockpi4 import *

elif board_id == ap_board.ROCK_PI_E:
    from adafruit_blinka.board.radxa.rockpie import *

elif board_id == ap_board.UDOO_X86:
    from adafruit_blinka.board.udoo_x86ultra import *

elif board_id == ap_board.STM32MP157C_DK2:
    from adafruit_blinka.board.stm32.stm32mp157c_dk2 import *

elif board_id == ap_board.OSD32MP1_RED:
    from adafruit_blinka.board.stm32.osd32mp1_red import *

elif board_id == ap_board.OSD32MP1_BRK:
    from adafruit_blinka.board.stm32.osd32mp1_brk import *

elif board_id == ap_board.LUBANCAT_IMX6ULL:
    from adafruit_blinka.board.lubancat.lubancat_imx6ull import *

elif board_id == ap_board.LUBANCAT_STM32MP157:
    from adafruit_blinka.board.lubancat.lubancat_stm32mp157 import *

elif board_id == ap_board.NANOPI_NEO_AIR:
    from adafruit_blinka.board.nanopi.neoair import *

elif board_id == ap_board.NANOPI_DUO2:
    from adafruit_blinka.board.nanopi.duo2 import *

elif board_id == ap_board.NANOPI_NEO:
    from adafruit_blinka.board.nanopi.neo import *

elif board_id == ap_board.PICO_U2IF:
    from adafruit_blinka.board.pico_u2if import *

elif board_id == ap_board.FEATHER_U2IF:
    from adafruit_blinka.board.feather_u2if import *

elif board_id == ap_board.QTPY_U2IF:
    from adafruit_blinka.board.qtpy_u2if import *

elif board_id == ap_board.ITSYBITSY_U2IF:
    from adafruit_blinka.board.itsybitsy_u2if import *

elif board_id == ap_board.MACROPAD_U2IF:
    from adafruit_blinka.board.macropad_u2if import *

elif board_id == ap_board.QT2040_TRINKEY_U2IF:
    from adafruit_blinka.board.qt2040_trinkey_u2if import *

elif board_id == ap_board.LICHEE_RV:
    from adafruit_blinka.board.lichee_rv import *

elif board_id == ap_board.SIEMENS_SIMATIC_IOT2050_ADV:
    from adafruit_blinka.board.siemens.siemens_iot2050 import *

elif board_id == ap_board.AML_S905X_CC:
    from adafruit_blinka.board.librecomputer.aml_s905x_cc_v1 import *

elif "sphinx" in sys.modules:
    pass

elif board_id is None:
    import platform
    import pkg_resources

    package = str(pkg_resources.get_distribution("adafruit_platformdetect")).split()
    raise NotImplementedError(
        "{1} version {2} was unable to identify the board and/or microcontroller running "
        "the {0} platform. Please be sure you have the latest packages running: 'pip3 install "
        "--upgrade adafruit-blinka adafruit-platformdetect'".format(
            platform.system(), package[0], package[1]
        )
    )

else:
    raise NotImplementedError("Board not supported {}".format(board_id))

if "SCL" in locals() and "SDA" in locals():

    def I2C():
        """The singleton I2C interface"""
        import busio

        return busio.I2C(SCL, SDA)


if "SCLK" in locals() and "MOSI" in locals() and "MISO" in locals():

    def SPI():
        """The singleton SPI interface"""
        import busio

        return busio.SPI(SCLK, MOSI, MISO)
