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
PG16 = pin.PG16
PG15 = pin.PG15
PG19 = pin.PG19
PG6 = pin.PG6
PG7 = pin.PG7
PH2 = pin.PH2
PG11 = pin.PG11
PH3 = pin.PH3
PG2 = pin.PG2
PG8 = pin.PG8
PG9 = pin.PG9
PH7 = pin.PH7
PH8 = pin.PH8
PG1 = pin.PG1
PH6 = pin.PH6
PH5 = pin.PH5
PH9 = pin.PH9
PG18 = pin.PG18
PG17 = pin.PG17
PG3 = pin.PG3
PG4 = pin.PG4
PG0 = pin.PG0
PG5 = pin.PG5
PG12 = pin.PG12
PH4 = pin.PH4
PG10 = pin.PG10
PG14 = pin.PG14
PG13 = pin.PG13
