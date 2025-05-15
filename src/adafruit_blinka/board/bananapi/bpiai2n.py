# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Banana Pi AI2N."""

from adafruit_blinka.microcontroller.renesas.rzv2n import pin

# I2C
I2C1_SCL = pin.I2C1_SCL
I2C1_SDA = pin.I2C1_SDA
I2C2_SCL = pin.I2C2_SCL
I2C2_SDA = pin.I2C2_SDA

# Default I2C
SCL = I2C1_SCL
SDA = I2C1_SDA

# UART
UART0_TX = pin.UART0_TX
UART0_RX = pin.UART0_RX
UART2_TX = pin.UART2_TX
UART2_RX = pin.UART2_RX

# Default UART
TX = UART2_TX
RX = UART2_RX
TXD = UART2_TX
RXD = UART2_RX

# SPI
SPI0_MOSI = pin.SPI0_MOSI
SPI0_MISO = pin.SPI0_MISO
SPI0_SCLK = pin.SPI0_SCLK
SPI0_CS0 = pin.SPI0_CS0
SPI2_MOSI = pin.SPI2_MOSI
SPI2_MISO = pin.SPI2_MISO
SPI2_SCLK = pin.SPI2_SCLK
SPI2_CS0 = pin.SPI2_CS0

# Default SPI
MOSI = SPI2_MOSI
MISO = SPI2_MISO
SCLK = SPI2_SCLK
CS = SPI2_CS0

# Pinout:
D3 = pin.P3_2
D5 = pin.P3_3
D7 = pin.P8_4
D8 = pin.P5_4
D10 = pin.P5_5
D11 = pin.P9_0
D12 = pin.P1_2
D13 = pin.P9_1
D15 = pin.P9_2
D16 = pin.P5_7
D18 = pin.P5_6
D19 = pin.PB_4
D21 = pin.PB_3
D22 = pin.P5_3
D23 = pin.PB_5
D24 = pin.PA_7
D26 = pin.PA_6
D27 = pin.P2_0
D28 = pin.P2_1
D29 = pin.P9_3
D31 = pin.P2_1
D32 = pin.P5_0
D33 = pin.P5_2
D35 = pin.P1_3
D36 = pin.P5_1
D37 = pin.P9_7
D38 = pin.P1_5
D40 = pin.P0_4
