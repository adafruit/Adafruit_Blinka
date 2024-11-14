# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Banana Pi F3."""

from adafruit_blinka.microcontroller.spacemit.k1 import pin

# I2C
I2C4_SCL = pin.I2C4_SCL
I2C4_SDA = pin.I2C4_SDA

# Default I2C
SCL = I2C4_SCL
SDA = I2C4_SDA

# UART
UART0_TX = pin.UART0_TX
UART0_RX = pin.UART0_RX

# Default UART
TX = UART0_TX
RX = UART0_RX
TXD = UART0_TX
RXD = UART0_RX

# SPI
SPI3_MOSI = pin.SPI3_MOSI
SPI3_MISO = pin.SPI3_MISO
SPI3_SCLK = pin.SPI3_SCLK
SPI3_CS0 = pin.SPI3_CS0

# Default SPI
MOSI = SPI3_MOSI
MISO = SPI3_MISO
SCLK = SPI3_SCLK
CS = SPI3_CS0

# Pinout reference:
# https://wiki.banana-pi.org/Banana_Pi_BPI-M4_Berry#BPI-M4_Berry_40-pin_header
D3 = pin.GPIO_52
D5 = pin.GPIO_51
D7 = pin.GPIO_70
D8 = pin.GPIO_47
D10 = pin.GPIO_48
D11 = pin.GPIO_71
D12 = pin.GPIO_74
D13 = pin.GPIO_72
D15 = pin.GPIO_73
D16 = pin.GPIO_91
D18 = pin.GPIO_92
D19 = pin.GPIO_77
D21 = pin.GPIO_78
D22 = pin.GPIO_49
D23 = pin.GPIO_75
D24 = pin.GPIO_76
D26 = pin.GPIO_50
