# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Banana Pi M4 Zero."""

from adafruit_blinka.microcontroller.allwinner.h618 import pin

# I2C
I2C0_SCL = pin.TWI0_SCL
I2C0_SDA = pin.TWI0_SDA
I2C1_SCL = pin.TWI1_SCL
I2C1_SDA = pin.TWI1_SDA

# Default I2C
SCL = I2C0_SCL
SDA = I2C0_SDA

# UART
UART4_TX = pin.UART4_TX
UART4_RX = pin.UART4_RX
UART5_TX = pin.UART5_TX
UART5_RX = pin.UART5_RX

# Default UART
TX = UART4_TX
RX = UART4_RX
TXD = UART4_TX
RXD = UART4_RX

# SPI
SPI1_MOSI = pin.SPI1_MOSI
SPI1_MISO = pin.SPI1_MISO
SPI1_SCLK = pin.SPI1_SCLK
SPI1_CS0 = pin.SPI1_CS0

# Default SPI
MOSI = SPI1_MOSI
MISO = SPI1_MISO
SCLK = SPI1_SCLK
CS = SPI1_CS0

# Pinout reference:
# https://wiki.banana-pi.org/Banana_Pi_BPI-M4_Zero#BPI-M4_Zero_40-pin_header
D3 = pin.PI6
D5 = pin.PI5
D7 = pin.PI12
D8 = pin.PI13
D10 = pin.PI14
D11 = pin.PH2
D12 = pin.PI1
D13 = pin.PH3
D15 = pin.PI11
D16 = pin.PI15
D18 = pin.PI16
D19 = pin.PH7
D21 = pin.PH8
D22 = pin.PC2
D23 = pin.PH6
D24 = pin.PH5
D26 = pin.PH9
D27 = pin.PI8
D28 = pin.PI7
D29 = pin.PI10
D31 = pin.PI9
D32 = pin.PH4
D33 = pin.PH10
D35 = pin.PI2
D36 = pin.PC7
D37 = pin.PI0
D38 = pin.PI4
D40 = pin.PI3
