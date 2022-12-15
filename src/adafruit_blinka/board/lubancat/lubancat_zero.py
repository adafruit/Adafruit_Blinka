# SPDX-FileCopyrightText: 2022 mmontol
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the LubanCat zero."""

from adafruit_blinka.microcontroller.rockchip.rk3566 import pin

# lbancat zero board 40-pin  J8 or J7:
# --------------------------
# 3V3   | (1)  (2)  | 5V
# GPIO3 | (3)  (4)  | 5V
# GPIO5 | (5)  (6)  | GND
# GPIO7 | (7)  (8)  | GPIO8
# GND   | (9)  (10) | GPIO10
# .......................
# .......................
# GPIO33| (33) (34) | GND
# GPIO35| (35) (36) | GPIO36
# GPIO37| (37) (38) | GPIO38
# GND   | (39) (40) | GPIO40
# --------------------------

GPIO3 = pin.GPIO1_A0
GPIO5 = pin.GPIO1_A1
GPIO7 = pin.GPIO1_A2
GPIO8 = pin.GPIO2_C5
GPIO10 = pin.GPIO2_C6
GPIO11 = pin.GPIO1_A3
GPIO12 = pin.GPIO0_C2
GPIO13 = pin.GPIO1_A4
GPIO15 = pin.GPIO1_A5
GPIO16 = pin.GPIO2_C3
GPIO18 = pin.GPIO2_C4
GPIO19 = pin.GPIO4_C3
GPIO21 = pin.GPIO4_C5
GPIO22 = pin.GPIO1_B0
GPIO23 = pin.GPIO4_C2
GPIO24 = pin.GPIO4_C6
GPIO26 = pin.GPIO1_B3
GPIO27 = pin.GPIO3_B4
GPIO28 = pin.GPIO3_B3
GPIO29 = pin.GPIO1_A7
GPIO31 = pin.GPIO1_B0
GPIO32 = pin.GPIO3_B6
GPIO33 = pin.GPIO3_B1
GPIO35 = pin.GPIO3_B2
GPIO36 = pin.GPIO3_A5
GPIO37 = pin.GPIO1_B1
GPIO38 = pin.GPIO3_A6
GPIO40 = pin.GPIO3_A7

# I2C3
I2C3_SDA = pin.I2C3_SDA_M0
I2C3_SCL = pin.I2C3_SCL_M0
I2C5_SCL = pin.I2C5_SCL_M0
I2C5_SDA = pin.I2C5_SDA_M0

# UART
UART8_TX = pin.UART8_TX_M0
UART8_RX = pin.UART8_RX_M0

# SPI
MOSI = pin.SPI3_MOSI_M0
MISO = pin.SPI3_MISO_M0
SCLK = pin.SPI3_CLK_M0
CS0 = pin.SPI3_CS0_M1
CS1 = pin.GPIO1_B3

# PWM
