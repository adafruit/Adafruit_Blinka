# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the PineH64."""

from adafruit_blinka.microcontroller.allwinner.h6 import pin

D2 = pin.PD26
D3 = pin.PD25
D4 = pin.PL8
D5 = pin.PH2
D6 = pin.PG14
D7 = pin.PC16
D8 = pin.PH3
D9 = pin.PH6
D10 = pin.PH5
D11 = pin.PH4
D12 = pin.PD22
D13 = pin.PD21
D14 = pin.PD19
D15 = pin.PD20
D16 = pin.PD24
D17 = pin.PL9
D18 = pin.PG11
D19 = pin.PG10
D21 = pin.PG12
D22 = pin.PG13
D23 = pin.PD16
D24 = pin.PD17
D25 = pin.PD18
D26 = pin.PD23
D27 = pin.PD14

SDA = D2
SCL = D3

SCLK = D11
MOSI = D10
MISO = D9
CS = D8
SCK = SCLK

UART_TX = D14
UART_RX = D15
