# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Clockwork Pi (CPI3) board."""

from adafruit_blinka.microcontroller.allwinner.a33 import pin

# Clockwork Pi GPIO port (DEBUG section in datasheet)

# Type 	Pin # (ext.) 	Pin # (Package) 	Function 1 	Function 2 	Pin # (sysfs) 	Color
# 3V0 	1 											blue
# GPIO 	2 		PB0 			UART0/2_TX 	PB-EINT0 	32 		green
# GPIO 	3 		PB1 			UART0/2_RX 	PB-EINT1 	33 		yellow
# GND 	4 											white
# GPIO 	5 		PH5 			I2C1-SDA 			229 		red
# GPIO 	6 		PH4 			I2C1-SCL 			228 		brown
# GND 	7 											black
# GPIO 	8 		PH6 			UART3-TX 	SPI0-CS 	230 		blue
# GPIO	9 		PH7 			UART3-RX 	SPI0-CLK 	231 		green
# GPIO 	10 		PH9 			UART3-CTS 	SPI0-MISO 	233 		yellow
# GPIO 	11 		PH8 			UART3-RTS 	SPI0-MOSI 	232 		white
# GND 	12 											red
# 5V0 	13 											brown
# 5V0 	14 											black

PB0 = pin.PB0
PB1 = pin.PB1
TX = PB0
RX = PB1

SCL = pin.PH4
SDA = pin.PH5

SCLK = pin.PH7
MOSI = pin.PH8
MISO = pin.PH9
