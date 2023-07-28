# SPDX-FileCopyrightText: 2022 Corebb
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Orange Pi 5"""

from adafruit_blinka.microcontroller.rockchip.rk3588 import pin

# D pin number is ordered by physical pin sequence

# D1 = +3.3V
# D2 = +5V
D3 = pin.GPIO1_B7
# D4 = +5V
D5 = pin.GPIO1_B6
# D6 = GND
D7 = pin.GPIO1_C6
D8 = pin.GPIO4_A3
# D9 = GND
D10 = pin.GPIO4_A4
D11 = pin.GPIO4_B2
D12 = pin.GPIO0_D5
D13 = pin.GPIO4_B3
# D14 = GND
D15 = pin.GPIO0_D4
D16 = pin.GPIO1_D3
# D17 = +3.3V
D18 = pin.GPIO1_D2
D19 = pin.GPIO1_C1
# D20 = GND
D21 = pin.GPIO1_C0
D22 = pin.GPIO2_D4
D23 = pin.GPIO1_C2
D24 = pin.GPIO1_C4
# D25 = GND
D26 = pin.GPIO1_A3

# UART
UART0_TX = pin.GPIO4_A3
UART0_RX = pin.GPIO4_A4
UART1_TX = pin.GPIO1_B6
UART1_RX = pin.GPIO1_B7
UART3_TX = pin.GPIO1_C1
UART3_RX = pin.GPIO1_C0
UART4_TX = pin.GPIO1_D2
UART4_RX = pin.GPIO1_D3

# Default UART
TX = UART1_TX
RX = UART1_RX
TXD = UART1_TX
RXD = UART1_RX

# I2C
I2C1_SCL = pin.GPIO1_B1
I2C1_SDA = pin.GPIO1_B2
I2C3_SCL = pin.GPIO1_C1
I2C3_SDA = pin.GPIO1_C0
I2C5_SCL = pin.GPIO1_B6
I2C5_SDA = pin.GPIO1_B7

# Default I2C
SCL = I2C1_SCL
SDA = I2C1_SDA

# SPI
SPI4_MISO = pin.GPIO1_C0
SPI4_MOSI = pin.GPIO1_C1
SPI4_CLK = pin.GPIO1_C2
SPI4_CS1 = pin.GPIO1_C4

# Default SPI
MOSI = SPI4_MOSI
MISO = SPI4_MISO
SCLK = SPI4_CLK
CS = SPI4_CS1
