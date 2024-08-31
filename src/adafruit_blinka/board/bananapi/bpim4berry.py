# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Banana Pi M4 Berry."""

from adafruit_blinka.microcontroller.allwinner.h618 import pin

# I2C
I2C3_SCL = pin.TWI3_SCL
I2C3_SDA = pin.TWI3_SDA
I2C4_SCL = pin.TWI4_SCL
I2C4_SDA = pin.TWI4_SDA

# Default I2C
SCL = I2C4_SCL
SDA = I2C4_SDA

# UART
UART1_TX = pin.UART1_TX
UART1_RX = pin.UART1_RX
UART5_TX = pin.UART5_TX
UART5_RX = pin.UART5_RX

# Default UART
TX = UART1_TX
RX = UART1_RX
TXD = UART1_TX
RXD = UART1_RX

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
# https://wiki.banana-pi.org/Banana_Pi_BPI-M4_Berry#BPI-M4_Berry_40-pin_header
D3 = pin.PG16
D5 = pin.PG15
D7 = pin.PG19
D8 = pin.PG6
D10 = pin.PG7
D11 = pin.PH2
D12 = pin.PG11
D13 = pin.PH3
D15 = pin.PG2
D16 = pin.PG8
D18 = pin.PG9
D19 = pin.PH7
D21 = pin.PH8
D22 = pin.PG1
D23 = pin.PH6
D24 = pin.PH5
D26 = pin.PH9
D27 = pin.PG18
D28 = pin.PG17
D29 = pin.PG3
D31 = pin.PG4
D32 = pin.PG0
D33 = pin.PG5
D35 = pin.PG12
D36 = pin.PH4
D37 = pin.PG10
D38 = pin.PG14
D40 = pin.PG13
