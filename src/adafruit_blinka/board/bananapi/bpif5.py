# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Banana Pi F5."""

from adafruit_blinka.microcontroller.allwinner.t527 import pin

# I2C
I2C4_SCL = pin.I2C4_SCL
I2C4_SDA = pin.I2C4_SDA
I2C5_SCL = pin.I2C5_SCL
I2C5_SDA = pin.I2C5_SDA

# Default I2C
SCL = I2C5_SCL
SDA = I2C5_SDA

# UART
UART2_TX = pin.UART2_TX
UART2_RX = pin.UART2_RX
UART7_TX = pin.UART7_TX
UART7_RX = pin.UART7_RX

# Default UART
TX = UART7_TX
RX = UART7_RX
TXD = UART7_TX
RXD = UART7_RX

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
D3 = pin.PI9
D5 = pin.PI8
D7 = pin.PI10
D8 = pin.PB13
D10 = pin.PB14
D11 = pin.PB0
D12 = pin.PB5
D13 = pin.PB1
D15 = pin.PB2
D16 = pin.PB11
D18 = pin.PB12
D19 = pin.PI4
D21 = pin.PI5
D22 = pin.PI7
D23 = pin.PI3
D24 = pin.PI2
D26 = pin.PI6
D27 = pin.PI1
D28 = pin.PI0
D29 = pin.PB3
D31 = pin.PL4
D32 = pin.PI11
D33 = pin.PL5
D35 = pin.PB6
D36 = pin.PI12
D37 = pin.PB4
D38 = pin.PB8
D40 = pin.PB7
