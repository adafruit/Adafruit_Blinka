# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Radxa Zero."""

from adafruit_blinka.microcontroller.amlogic.s905y2 import pin

D3 = pin.GPIOA_14
D5 = pin.GPIOA_15
D7 = pin.GPIOAO_3
D8 = pin.GPIOAO_8
D10 = pin.GPIOAO_1
D11 = pin.GPIOAO_2
D12 = pin.GPIOX_9
D13 = pin.GPIOX_11
D16 = pin.GPIOX_10
D18 = pin.GPIOX_8
D19 = pin.GPIOH_4
D21 = pin.GPIOH_5
D23 = pin.GPIOH_7
D24 = pin.GPIOH_6
D27 = pin.GPIOAO_3
D28 = pin.GPIOAO_2
D32 = pin.GPIOAO_4
D35 = pin.GPIOAO_8
D36 = pin.GPIOH_8
D37 = pin.GPIOAO_9
D38 = pin.GPIOAO_10
D40 = pin.GPIOAO_11

SDA1 = D24
SCL1 = D23

SDA3 = D3
SCL3 = D5

SDA4 = D27
SCL4 = D28

SCLK = D13
MOSI = D18
MISO = D12

SCLK1 = D23
MOSI1 = D19
MISO1 = D21

UART_TX = D11
UART_RX = D7

UART_TX1 = D18
UART_RX1 = D12

UART_TX4 = D23
UART_RX4 = D24
