# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the STM32MP157C Development Kit 2."""

from adafruit_blinka.microcontroller.stm32.stm32mp157 import pin

D2 = pin.PA12
D3 = pin.PA11
D4 = pin.PA8
D5 = pin.PG2
D6 = pin.PH11
D7 = pin.PF3
D8 = pin.PF6
D9 = pin.PF8
D10 = pin.PF9
D11 = pin.PF7
D12 = pin.PD13
D13 = pin.PC7
D14 = pin.PB10
D15 = pin.PB12
D16 = pin.PB13
D17 = pin.PG8
D18 = pin.PI5
D19 = pin.PI7
D20 = pin.PI6
D21 = pin.PF11
D22 = pin.PG15
D23 = pin.PF1
D24 = pin.PF0
D25 = pin.PF4
D26 = pin.PF5
D27 = pin.PD7

SDA = D2
SCL = D3

SDA1 = pin.PF15
SCL1 = pin.PD12

SCLK = D11
MOSI = D10
MISO = D9

CE0 = D8
CE1 = D7

CS = CE0
SCK = SCLK

UART_TX = D14
UART_RX = D15
