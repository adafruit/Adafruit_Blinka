# SPDX-FileCopyrightText: 2025 fb0u
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Radxa Rock 3B."""

from adafruit_blinka.microcontroller.rockchip.rk3568 import pin

# 3B IO pins

D1_A0 = pin.GPIO1_A0
D1_A1 = pin.GPIO1_A1
D0_B5 = pin.GPIO0_B5
D0_D1 = pin.GPIO0_D1
D0_D0 = pin.GPIO0_D0
D3_C4 = pin.GPIO3_C4
D3_A3 = pin.GPIO3_A3
D3_C5 = pin.GPIO3_C5
D0_C0 = pin.GPIO0_C0
D0_B6 = pin.GPIO0_B6
D3_B2 = pin.GPIO3_B2
D4_C3 = pin.GPIO4_C3
D4_C5 = pin.GPIO4_C5
D0_C1 = pin.GPIO0_C1
D4_C2 = pin.GPIO4_C2
D4_C6 = pin.GPIO4_C6
D4_D1 = pin.GPIO4_D1
D2_D7 = pin.GPIO2_D7
D3_A0 = pin.GPIO3_A0
D3_C2 = pin.GPIO3_C2
D3_C3 = pin.GPIO3_C3
D3_A4 = pin.GPIO3_A4
D3_A2 = pin.GPIO3_A2
D3_A6 = pin.GPIO3_A6
D3_A5 = pin.GPIO3_A5

# I2C (use I2C3)
SDA = D1_A0
SCL = D1_A1

# SPI (use SPI3)
CE0 = D4_C6
SCLK = D4_C2
SCK = D4_C2
MOSI = D4_C3
MISO = D4_C5

# UART aliases (use UART2)
UART_TX = D0_D1
UART_RX = D0_D0
TXD = D0_D1
RXD = D0_D0
TX = D0_D1
RX = D0_D0
