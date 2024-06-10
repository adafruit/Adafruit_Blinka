# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
G12A, G12B, and SM1 Common Definitions
Ref:
Linux kernel 4.9.y (hardkernel)
    linux/include/dt-bindings/gpio/meson-g12a-gpio.h
Linux kernel 5.4.y (mainline)
    linux/include/dt-bindings/gpio/meson-g12a-gpio.h
    linux/arch/arm64/boot/dts/amlogic/meson-g12-common.dtsi
"""

import gpiod
from adafruit_blinka.microcontroller.alias import get_dts_alias
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

chip0 = gpiod.Chip("0")
chip1 = gpiod.Chip("1")

if chip0.num_lines() < 20:
    aobus = 0
    periphs = 1
    periphs_offset = chip1.num_lines() - 85
else:
    aobus = 1
    periphs = 0
    periphs_offset = chip0.num_lines() - 85

chip0.close()
chip1.close()

GPIOAO_0 = GPIO496 = Pin((aobus, 0))
GPIOAO_1 = GPIO497 = Pin((aobus, 1))
GPIOAO_2 = GPIO498 = Pin((aobus, 2))
GPIOAO_3 = GPIO499 = Pin((aobus, 3))
GPIOAO_4 = GPIO500 = Pin((aobus, 4))
GPIOAO_5 = GPIO501 = Pin((aobus, 5))
GPIOAO_6 = GPIO502 = Pin((aobus, 6))
GPIOAO_7 = GPIO503 = Pin((aobus, 7))
GPIOAO_8 = GPIO504 = Pin((aobus, 8))
GPIOAO_9 = GPIO505 = Pin((aobus, 9))
GPIOAO_10 = GPIO506 = Pin((aobus, 10))
GPIOAO_11 = GPIO507 = Pin((aobus, 11))

GPIOE_0 = GPIO508 = Pin((aobus, 12))
GPIOE_1 = GPIO509 = Pin((aobus, 13))
GPIOE_2 = GPIO510 = Pin((aobus, 14))

GPIOZ_0 = GPIO427 = Pin((periphs, 0 + periphs_offset))
GPIOZ_1 = GPIO428 = Pin((periphs, 1 + periphs_offset))
GPIOZ_2 = GPIO429 = Pin((periphs, 2 + periphs_offset))
GPIOZ_3 = GPIO430 = Pin((periphs, 3 + periphs_offset))
GPIOZ_4 = GPIO431 = Pin((periphs, 4 + periphs_offset))
GPIOZ_5 = GPIO432 = Pin((periphs, 5 + periphs_offset))
GPIOZ_6 = GPIO433 = Pin((periphs, 6 + periphs_offset))
GPIOZ_7 = GPIO434 = Pin((periphs, 7 + periphs_offset))
GPIOZ_8 = GPIO435 = Pin((periphs, 8 + periphs_offset))
GPIOZ_9 = GPIO436 = Pin((periphs, 9 + periphs_offset))
GPIOZ_10 = GPIO437 = Pin((periphs, 10 + periphs_offset))
GPIOZ_11 = GPIO438 = Pin((periphs, 11 + periphs_offset))
GPIOZ_12 = GPIO439 = Pin((periphs, 12 + periphs_offset))
GPIOZ_13 = GPIO440 = Pin((periphs, 13 + periphs_offset))
GPIOZ_14 = GPIO441 = Pin((periphs, 14 + periphs_offset))
GPIOZ_15 = GPIO442 = Pin((periphs, 15 + periphs_offset))

GPIOH_0 = GPIO443 = Pin((periphs, 16 + periphs_offset))
GPIOH_1 = GPIO444 = Pin((periphs, 17 + periphs_offset))
GPIOH_2 = GPIO445 = Pin((periphs, 18 + periphs_offset))
GPIOH_3 = GPIO446 = Pin((periphs, 19 + periphs_offset))
GPIOH_4 = GPIO447 = Pin((periphs, 20 + periphs_offset))
GPIOH_5 = GPIO448 = Pin((periphs, 21 + periphs_offset))
GPIOH_6 = GPIO449 = Pin((periphs, 22 + periphs_offset))
GPIOH_7 = GPIO450 = Pin((periphs, 23 + periphs_offset))
GPIOH_8 = GPIO451 = Pin((periphs, 24 + periphs_offset))

BOOT_0 = GPIO452 = Pin((periphs, 25 + periphs_offset))
BOOT_1 = GPIO453 = Pin((periphs, 26 + periphs_offset))
BOOT_2 = GPIO454 = Pin((periphs, 27 + periphs_offset))
BOOT_3 = GPIO455 = Pin((periphs, 28 + periphs_offset))
BOOT_4 = GPIO456 = Pin((periphs, 29 + periphs_offset))
BOOT_5 = GPIO457 = Pin((periphs, 30 + periphs_offset))
BOOT_6 = GPIO458 = Pin((periphs, 31 + periphs_offset))
BOOT_7 = GPIO459 = Pin((periphs, 32 + periphs_offset))
BOOT_8 = GPIO460 = Pin((periphs, 33 + periphs_offset))
BOOT_9 = GPIO461 = Pin((periphs, 34 + periphs_offset))
BOOT_10 = GPIO462 = Pin((periphs, 35 + periphs_offset))
BOOT_11 = GPIO463 = Pin((periphs, 36 + periphs_offset))
BOOT_12 = GPIO464 = Pin((periphs, 37 + periphs_offset))
BOOT_13 = GPIO465 = Pin((periphs, 38 + periphs_offset))
BOOT_14 = GPIO466 = Pin((periphs, 39 + periphs_offset))
BOOT_15 = GPIO467 = Pin((periphs, 40 + periphs_offset))

GPIOC_0 = GPIO468 = Pin((periphs, 41 + periphs_offset))
GPIOC_1 = GPIO469 = Pin((periphs, 42 + periphs_offset))
GPIOC_2 = GPIO470 = Pin((periphs, 43 + periphs_offset))
GPIOC_3 = GPIO471 = Pin((periphs, 44 + periphs_offset))
GPIOC_4 = GPIO472 = Pin((periphs, 45 + periphs_offset))
GPIOC_5 = GPIO473 = Pin((periphs, 46 + periphs_offset))
GPIOC_6 = GPIO474 = Pin((periphs, 47 + periphs_offset))
GPIOC_7 = GPIO475 = Pin((periphs, 48 + periphs_offset))

GPIOA_0 = GPIO460 = Pin((periphs, 49 + periphs_offset))
GPIOA_1 = GPIO461 = Pin((periphs, 50 + periphs_offset))
GPIOA_2 = GPIO462 = Pin((periphs, 51 + periphs_offset))
GPIOA_3 = GPIO463 = Pin((periphs, 52 + periphs_offset))
GPIOA_4 = GPIO464 = Pin((periphs, 53 + periphs_offset))
GPIOA_5 = GPIO465 = Pin((periphs, 54 + periphs_offset))
GPIOA_6 = GPIO466 = Pin((periphs, 55 + periphs_offset))
GPIOA_7 = GPIO467 = Pin((periphs, 56 + periphs_offset))
GPIOA_8 = GPIO468 = Pin((periphs, 57 + periphs_offset))
GPIOA_9 = GPIO469 = Pin((periphs, 58 + periphs_offset))
GPIOA_10 = GPIO470 = Pin((periphs, 59 + periphs_offset))
GPIOA_11 = GPIO471 = Pin((periphs, 60 + periphs_offset))
GPIOA_12 = GPIO472 = Pin((periphs, 61 + periphs_offset))
GPIOA_13 = GPIO473 = Pin((periphs, 62 + periphs_offset))
GPIOA_14 = GPIO474 = Pin((periphs, 63 + periphs_offset))
GPIOA_15 = GPIO475 = Pin((periphs, 64 + periphs_offset))

GPIOX_0 = GPIO476 = Pin((periphs, 65 + periphs_offset))
GPIOX_1 = GPIO477 = Pin((periphs, 66 + periphs_offset))
GPIOX_2 = GPIO478 = Pin((periphs, 67 + periphs_offset))
GPIOX_3 = GPIO479 = Pin((periphs, 68 + periphs_offset))
GPIOX_4 = GPIO480 = Pin((periphs, 69 + periphs_offset))
GPIOX_5 = GPIO481 = Pin((periphs, 70 + periphs_offset))
GPIOX_6 = GPIO482 = Pin((periphs, 71 + periphs_offset))
GPIOX_7 = GPIO483 = Pin((periphs, 72 + periphs_offset))
GPIOX_8 = GPIO484 = Pin((periphs, 73 + periphs_offset))
GPIOX_9 = GPIO485 = Pin((periphs, 74 + periphs_offset))
GPIOX_10 = GPIO486 = Pin((periphs, 75 + periphs_offset))
GPIOX_11 = GPIO487 = Pin((periphs, 76 + periphs_offset))
GPIOX_12 = GPIO488 = Pin((periphs, 77 + periphs_offset))
GPIOX_13 = GPIO489 = Pin((periphs, 78 + periphs_offset))
GPIOX_14 = GPIO490 = Pin((periphs, 79 + periphs_offset))
GPIOX_15 = GPIO491 = Pin((periphs, 80 + periphs_offset))
GPIOX_16 = GPIO492 = Pin((periphs, 81 + periphs_offset))
GPIOX_17 = GPIO493 = Pin((periphs, 82 + periphs_offset))
GPIOX_18 = GPIO494 = Pin((periphs, 83 + periphs_offset))
GPIOX_19 = GPIO495 = Pin((periphs, 84 + periphs_offset))

SPI0_SCLK = GPIOA_1
SPI0_MCLK0 = GPIOA_0
SPI0_SDO = GPIOA_3
SPI0_SDI = GPIOA_4

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI0_SCLK, SPI0_MCLK0, SPI0_SDO, SPI0_SDI),)

UART1_TX = GPIOH_7
UART1_RX = GPIOH_6

# ordered as uartId, txId, rxId
uartPorts = ((1, UART1_TX, UART1_RX),)

# ordered as i2cId, sclId, sdaId
i2cPorts = []

alias = get_dts_alias("ff805000.i2c")
if alias is not None:
    globals()[alias + "_SCL"] = GPIOX_18
    globals()[alias + "_SDA"] = GPIOX_17
    i2cPorts.append((int(alias[3]), GPIOX_18, GPIOX_17))

i2cPorts = tuple(i2cPorts)
