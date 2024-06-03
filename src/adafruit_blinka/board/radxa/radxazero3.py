# SPDX-FileCopyrightText: 2024 Burberius
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Radxa ZERO 3 (3E and 3W)"""

from adafruit_blinka.microcontroller.rockchip.rk3566 import pin

# ZERO 3 IO pins

D1_A0 = pin.GPIO1_A0
D1_A1 = pin.GPIO1_A1
D3_C4 = pin.GPIO3_C4
D3_A1 = pin.GPIO3_A1
D3_A2 = pin.GPIO3_A2
D3_B0 = pin.GPIO3_B0
D4_C3 = pin.GPIO4_C3
D4_C5 = pin.GPIO4_C5
D4_C2 = pin.GPIO4_C2
D4_B2 = pin.GPIO4_B2
D3_B3 = pin.GPIO3_B3
D3_B4 = pin.GPIO3_B4
D3_C3 = pin.GPIO3_C3
D3_A4 = pin.GPIO3_A4
D1_A4 = pin.GPIO1_A4
D0_D1 = pin.GPIO0_D1
D0_D0 = pin.GPIO0_D0
D3_A3 = pin.GPIO3_A3
D3_B1 = pin.GPIO3_B1
D3_B2 = pin.GPIO3_B2
D3_C1 = pin.GPIO3_C1
D4_C6 = pin.GPIO4_C6
D4_B3 = pin.GPIO4_B3
D3_C2 = pin.GPIO3_C2
D3_A7 = pin.GPIO3_A7
D3_A6 = pin.GPIO3_A6
D3_A5 = pin.GPIO3_A5


# I2C
SDA = D1_A0
SCL = D1_A1

# SPI
CE0 = D4_C6
SCLK = D4_C2
MOSI = D4_C3
MISO = D4_C5

# UART aliases
UART_TX = D0_D1
UART_RX = D0_D0
UART2_TX = UART_TX
UART2_RX = UART_RX
UART3_TX = D1_A1
UART3_RX = D1_A0
UART4_TX = D3_B2
UART4_RX = D3_B1
UART5_TX = D3_C2
UART5_RX = D3_C3
UART9_TX = D4_C5
UART9_RX = D4_C6
TXD = D0_D1
RXD = D0_D0
TX = D0_D1
RX = D0_D0
