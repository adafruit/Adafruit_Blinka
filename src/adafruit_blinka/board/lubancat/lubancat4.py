# SPDX-FileCopyrightText: 2023 mmontol
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the LubanCat-4."""

from adafruit_blinka.microcontroller.rockchip.rk3588 import pin

# lbancat4 board 40-Pin  J9:
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

# GPIO1 = +3.3V
# GPIO2 = +5V
GPIO3 = pin.GPIO1_B7
# GPIO4 = +5V
GPIO5 = pin.GPIO1_B6
# GPIO6 = GND
GPIO7 = pin.GPIO0_A0
GPIO8 = pin.GPIO4_A3
# GPIO9 = GND
GPIO10 = pin.GPIO4_A4
GPIO11 = pin.GPIO1_A1
GPIO12 = pin.GPIO1_D6
GPIO13 = pin.GPIO1_A7
# GPIO14 = GND
GPIO15 = pin.GPIO1_B0
GPIO16 = pin.GPIO3_C1
# GPIO17 = +3.3V
GPIO18 = pin.GPIO3_D2
GPIO19 = pin.GPIO1_B2
# GPIO20 = GND
GPIO21 = pin.GPIO1_B1
GPIO22 = pin.GPIO3_D4
GPIO23 = pin.GPIO1_B3
GPIO24 = pin.GPIO1_B4
# GPIO25 = GND
GPIO26 = pin.GPIO1_B5
GPIO27 = pin.GPIO4_B0
GPIO28 = pin.GPIO4_B1
GPIO29 = pin.GPIO3_A6
# GPIO30 = GND
GPIO31 = pin.GPIO3_B7
GPIO32 = pin.GPIO1_D7
GPIO33 = pin.GPIO3_D3
# GPIO34 = GND
GPIO35 = pin.GPIO3_D5
GPIO36 = pin.GPIO4_A0
GPIO37 = pin.GPIO3_C0
GPIO38 = pin.GPIO4_A1
# GPIO39 = GND
GPIO40 = pin.GPIO4_A2

# I2C
I2C5_SCL = pin.I2C5_SCL_M3
I2C5_SDA = pin.I2C5_SDA_M3
I2C6_SCL = pin.I2C6_SCL_M3
I2C6_SDA = pin.I2C6_SDA_M3

# UART
UART0_TX = pin.UART0_TX_M2
UART0_RX = pin.UART0_RX_M2

# Default SPI
MOSI = pin.SPI0_MOSI_M2
MISO = pin.SPI0_MISO_M2
SCLK = pin.SPI0_CLK_M2
CS0 = pin.SPI0_CS0_M2
CS1 = pin.SPI0_CS1_M2

# PWM
PWM10 = pin.PWM10_M2
PWM11 = pin.PWM11_IR_M3
PWM14 = pin.PWM14_M2
PWM15 = pin.PWM15_IR_M3
