# SPDX-FileCopyrightText: 2026 Marco Gulino
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Orange Pi 5"""

from adafruit_blinka.microcontroller.rockchip.rk3588 import pin

# D pin number is ordered by physical pin sequence

# D1 = +3.3V
# D2 = +5V
D3 = pin.GPIO0_C0
# D4 = +5V
D5 = pin.GPIO0_B7
# D6 = GND
D7 = pin.GPIO1_A7
D8 = pin.GPIO0_B5
# D9 = GND
D10 = pin.GPIO0_B6
D11 = pin.GPIO1_A0
D12 = pin.GPIO4_A6
D13 = pin.GPIO1_A1
# D14 = GND
D15 = pin.GPIO1_A2
D16 = pin.GPIO1_A3
# D17 = +3.3V
D18 = pin.GPIO1_A4
D19 = pin.GPIO1_B2
# D20 = GND
D21 = pin.GPIO1_B1
D22 = pin.GPIO1_B0
D23 = pin.GPIO1_B3
D24 = pin.GPIO1_B4
# D25 = GND
D26 = pin.GPIO1_B5
D27 = pin.GPIO4_C1
D28 = pin.GPIO4_C0
D29 = pin.GPIO3_C1
# D30 = GND
D31 = pin.GPIO3_B5
D32 = pin.GPIO4_B3
D33 = pin.GPIO3_B6
# D34 = GND
D35 = pin.GPIO3_C2
D36 = pin.GPIO4_B7
D37 = pin.GPIO4_A7
D38 = pin.GPIO3_C0
# D39 = GND
D40 = pin.GPIO3_B7


# UART
UART2_TX = pin.GPIO0_B5
UART2_RX = pin.GPIO0_B6
UART3_TX = pin.GPIO3_B5
UART3_RX = pin.GPIO3_B6
UART4_TX = pin.GPIO1_B2
UART4_RX = pin.GPIO1_B3
UART6_TX = pin.GPIO1_A0
UART6_RX = pin.GPIO1_A1

# Default UART
TX = UART2_TX
RX = UART2_RX
TXD = UART2_TX
RXD = UART2_RX

# I2C
I2C2_SCL = pin.GPIO0_B7
I2C2_SDA = pin.GPIO0_C0
I2C4_SCL = pin.GPIO1_A3
I2C4_SDA = pin.GPIO1_A2
I2C5_SCL = pin.GPIO4_A6
I2C5_SDA = pin.GPIO4_A7
I2C8_SDA = pin.GPIO4_C0
I2C8_SCL = pin.GPIO4_C1

# Default I2C
SCL = I2C2_SCL
SDA = I2C2_SDA

# SPI
SPI0_MISO = pin.GPIO1_B1
SPI0_MOSI = pin.GPIO1_B2
SPI0_CLK = pin.GPIO1_B3
SPI0_CS0 = pin.GPIO1_B4
SPI0_CS1 = pin.GPIO1_B5

SPI1_MISO = pin.GPIO3_C0
SPI1_MOSI = pin.GPIO3_B7
SPI1_CLK = pin.GPIO3_C1
SPI1_CS0 = pin.GPIO3_C2

SPI4_MISO = pin.GPIO1_A0
SPI4_MOSI = pin.GPIO1_A1
SPI4_CLK = pin.GPIO1_A2
SPI4_CS0 = pin.GPIO1_A3

# Default SPI
MOSI = SPI0_MOSI
MISO = SPI0_MISO
SCLK = SPI0_CLK
CS = SPI0_CS0
