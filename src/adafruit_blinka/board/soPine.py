# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the SoPine."""

from adafruit_blinka.microcontroller.allwinner.a64 import pin

D2 = pin.PH3
D3 = pin.PH2
D4 = pin.PL10
D5 = pin.PH5
D6 = pin.PH6
D7 = pin.PH7
D8 = pin.PC3
D9 = pin.PC1
D10 = pin.PC0
D11 = pin.PC2
D12 = pin.PC4
D13 = pin.PC5
D14 = pin.PB0
D15 = pin.PB1
D16 = pin.PC6
D17 = pin.PC7
D18 = pin.PC8
D19 = pin.PC9
D20 = pin.PC10
D21 = pin.PC11
D22 = pin.PC12
D23 = pin.PC13
D24 = pin.PC14
D25 = pin.PC15
D26 = pin.PC16
D27 = pin.PH9

SDA = D2
SCL = D3

SCL2 = pin.PL8
SDA2 = pin.PL9

SCLK = D11
MOSI = D10
MISO = D9
CS = D8
SCK = SCLK

UART_TX = D14
UART_RX = D15

UART3_TX = pin.PD0
UART3_RX = pin.PD1

UART4_TX = pin.PD2
UART4_RX = pin.PD3
