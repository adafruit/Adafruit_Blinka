# SPDX-FileCopyrightText: 2023 mmontol
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the LubanCat2."""

from adafruit_blinka.microcontroller.rockchip.rk3568 import pin

# lbancat2 board 40-pin  J5:
# --------------------------
# 3V3   | (1)  (2)  | 5V
# GPIO3 | (3)  (4)  | 5V
# GPIO5 | (5)  (6)  | GND
# GPIO7 | (7)  (8)  | GPIO8
# GND   | (9)  (10) | GPIO10
# .......................  #
# .......................  #
# GPIO33| (33) (34) | GND
# GPIO35| (35) (36) | GPIO36
# GPIO37| (37) (38) | GPIO38
# GND   | (39) (40) | GPIO40
# --------------------------

GPIO3 = pin.GPIO1_A0
GPIO5 = pin.GPIO1_A1
GPIO7 = pin.GPIO0_B0
GPIO8 = pin.GPIO3_B7
GPIO10 = pin.GPIO3_C0
GPIO11 = pin.GPIO3_A5
GPIO12 = pin.GPIO3_B1
GPIO13 = pin.GPIO3_A6
GPIO15 = pin.GPIO3_A7
GPIO16 = pin.GPIO2_D7
GPIO18 = pin.GPIO3_A0
GPIO19 = pin.GPIO4_C3
GPIO21 = pin.GPIO4_C5
GPIO22 = pin.GPIO0_C2
GPIO23 = pin.GPIO4_C2
GPIO24 = pin.GPIO4_C6
GPIO26 = pin.GPIO4_C4
GPIO27 = pin.GPIO3_B4
GPIO28 = pin.GPIO3_B3
GPIO29 = pin.GPIO4_D2
GPIO31 = pin.GPIO3_B6
GPIO32 = pin.GPIO3_B2
GPIO33 = pin.GPIO3_B5
GPIO35 = pin.GPIO3_C4
GPIO36 = pin.GPIO1_B0
GPIO37 = pin.GPIO3_C5
GPIO38 = pin.GPIO1_B1
GPIO40 = pin.GPIO1_B2

# I2C
I2C3_SDA = pin.I2C3_SDA_M0
I2C3_SCL = pin.I2C3_SCL_M0
I2C5_SCL = pin.I2C5_SCL_M0
I2C5_SDA = pin.I2C5_SDA_M0

# UART
UART3_TX = pin.UART3_TX_M1
UART3_RX = pin.UART3_RX_M1

# SPI
MOSI = pin.SPI3_MOSI_M1
MISO = pin.SPI3_MISO_M1
SCLK = pin.SPI3_CLK_M1
CS0 = pin.GPIO4_C6
CS1 = pin.GPIO4_C4

# PWM
PWM8 = pin.PWM8_M0
PWM9 = pin.PWM9_M0
PWM10 = pin.PWM10_M0
PWM14 = pin.PWM14_M0
