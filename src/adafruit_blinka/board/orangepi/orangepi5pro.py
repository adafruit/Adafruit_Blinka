# SPDX-FileCopyrightText: 2022 Corebb
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Orange Pi 5 Pro"""

from adafruit_blinka.microcontroller.rockchip.rk3588 import pin

# D pin number is ordered by physical pin sequence

# D1 = +3.3V
# D2 = +5V
D3 = pin.GPIO1_D3
# D4 = +5V
D5 = pin.GPIO1_D2
# D6 = GND
D7 = pin.GPIO1_B7
D8 = pin.GPIO0_B5
# D9 = GND
D10 = pin.GPIO0_B6
D11 = pin.GPIO4_B2
D12 = pin.GPIO1_A7
D13 = pin.GPIO4_B3
# D14 = GND
D15 = pin.GPIO1_B6
D16 = pin.GPIO1_A1
# D17 = +3.3V
D18 = pin.GPIO1_A0
D19 = pin.GPIO1_B2
# D20 = GND
D21 = pin.GPIO1_B1
D22 = pin.GPIO1_B0
D23 = pin.GPIO1_B3
D24 = pin.GPIO1_B4
# D25 = GND
D26 = pin.GPIO1_B5
D27 = pin.GPIO1_A2
D28 = pin.GPIO1_A3
D29 = pin.GPIO1_A4
# D30 = GND
D31 = pin.GPIO1_A6
D32 = pin.GPIO1_D6
D33 = pin.GPIO1_D7
# D34 = GND
D35 = pin.GPIO4_A7
D36 = pin.GPIO4_A3
D37 = pin.GPIO4_A6
D38 = pin.GPIO4_A4
# D39 = GND
D40 = pin.GPIO4_A5

# UART
UART0_TX = pin.GPIO4_A3
UART0_RX = pin.GPIO4_A4
UART1_TX = pin.GPIO1_B6
UART1_RX = pin.GPIO1_B7
UART3_TX = pin.GPIO4_A5
UART3_RX = pin.GPIO4_A6
UART4_TX = pin.GPIO1_D2
UART4_RX = pin.GPIO1_D3

# Default UART
TX = UART0_TX
RX = UART0_RX
TXD = UART0_TX
RXD = UART0_RX

# I2C
I2C1_SCL = pin.GPIO1_D2
I2C1_SDA = pin.GPIO1_D3
I2C4_SCL = pin.GPIO1_A3
I2C4_SDA = pin.GPIO1_A2
I2C5_SCL = pin.GPIO1_B6
I2C5_SDA = pin.GPIO1_B7
I2C8_SCL = pin.GPIO1_D6
I2C8_SDA = pin.GPIO1_D7

# Default I2C
SCL = I2C1_SCL
SDA = I2C1_SDA

# SPI
SPI0_MISO = pin.GPIO1_B1
SPI0_MOSI = pin.GPIO1_B2
SPI0_CLK = pin.GPIO1_B3
SPI0_CS0 = pin.GPIO1_B4
SPI0_CS1 = pin.GPIO1_B5
SPI4_MISO = pin.GPIO1_A0
SPI4_MOSI = pin.GPIO1_A1
SPI4_CLK = pin.GPIO1_A2
SPI4_CS0 = pin.GPIO1_A3

# Default SPI
MOSI = SPI0_MOSI
MISO = SPI0_MISO
SCLK = SPI0_CLK
CS = SPI0_CS1
