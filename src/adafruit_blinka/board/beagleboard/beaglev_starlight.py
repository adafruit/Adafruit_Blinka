# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the BeagleV StarLight."""

from adafruit_blinka.microcontroller.starfive.JH71x0 import pin

D0 = pin.D0
D1 = pin.D1

SDA = pin.I2C2_SDA
SCL = pin.I2C2_SCL

D4 = pin.D4
D5 = pin.D5
D6 = pin.D6

D7 = pin.D7
CE1 = pin.D7
D8 = pin.D8
CE0 = pin.D8
D9 = pin.D9
MISO = pin.SPI_MISO
D10 = pin.D10
MOSI = pin.SPI_MOSI
D11 = pin.D11
SCLK = pin.SPI_SCLK
SCK = pin.SPI_SCLK

D12 = pin.D12
D13 = pin.D13

D14 = pin.D14
TXD = pin.UART_TX
D15 = pin.D15
RXD = pin.UART_RX
# create alias for most of the examples
TX = pin.UART_TX
RX = pin.UART_RX

D16 = pin.D16
D17 = pin.D17
D18 = pin.D18
D19 = pin.D19
D20 = pin.D20
D21 = pin.D21
D22 = pin.D22
D23 = pin.D23
D24 = pin.D24
D25 = pin.D25
D26 = pin.D26
D27 = pin.D27
