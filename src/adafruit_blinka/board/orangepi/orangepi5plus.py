# SPDX-FileCopyrightText: 2022 Corebb
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Orange Pi 5 Plus"""

from adafruit_blinka.microcontroller.rockchip.rk3588 import pin

# D pin number is ordered by physical pin sequence

# D1 = +3.3V
# D2 = +5V
D3 = pin.GPIO0_C0
# D4 = +5V
D5 = pin.GPIO0_B7
# D6 = GND
D7 = pin.GPIO1_D6
D8 = pin.GPIO1_A1
# D9 = GND
D10 = pin.GPIO1_A0
D11 = pin.GPIO1_A4
D12 = pin.GPIO3_A1
D13 = pin.GPIO1_A7
# D14 = GND
D15 = pin.GPIO1_B0
D16 = pin.GPIO3_B5
# D17 = +3.3V
D18 = pin.GPIO3_B6
D19 = pin.GPIO1_B2
# D20 = GND
D21 = pin.GPIO1_B1
D22 = pin.GPIO1_A2
D23 = pin.GPIO1_B3
D24 = pin.GPIO1_B4
# D25 = GND
D26 = pin.GPIO1_B5
D27 = pin.GPIO1_B7
D28 = pin.GPIO1_B6
D29 = pin.GPIO1_D7
# D30 = GND
D31 = pin.GPIO3_A0
D32 = pin.GPIO1_A3
D33 = pin.GPIO3_C2
# D34 = GND
D35 = pin.GPIO3_A2
D36 = pin.GPIO3_A5
D37 = pin.GPIO3_C1
D38 = pin.GPIO3_A4
# D39 = GND
D40 = pin.GPIO3_A3

# UART
UART1_TX = pin.GPIO1_B6
UART1_RX = pin.GPIO1_B7
UART3_TX = pin.GPIO3_B5
UART3_RX = pin.GPIO3_B6
UART4_TX = pin.GPIO1_B3
UART4_RX = pin.GPIO1_B2
UART6_TX = pin.GPIO1_A1
UART6_RX = pin.GPIO1_A0
UART7_TX = pin.GPIO1_B5
UART7_RX = pin.GPIO1_B4
UART8_TX = pin.GPIO3_A2
UART8_RX = pin.GPIO3_A3

# Default UART
TX = UART1_TX
RX = UART1_RX
TXD = UART1_TX
RXD = UART1_RX

# I2C
I2C2_SCL = pin.GPIO0_B7
I2C2_SDA = pin.GPIO0_C0
I2C4_SCL = pin.GPIO1_A3
I2C4_SDA = pin.GPIO1_A2
I2C5_SCL = pin.GPIO1_B6
I2C5_SDA = pin.GPIO1_B7
I2C8_SCL = pin.GPIO1_D6
I2C8_SDA = pin.GPIO1_D7

# Default I2C
SCL = I2C2_SCL
SDA = I2C2_SDA

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
SPI4_CS1 = pin.GPIO1_A4

# Default SPI
MOSI = SPI0_MOSI
MISO = SPI0_MISO
SCLK = SPI0_CLK
CS = SPI0_CS1
