# SPDX-FileCopyrightText: 2024 Hajime Fujimoto
#
# SPDX-License-Identifier: MIT
"""A Pin class for use with Horizon Sunrise X3."""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

D0 = Pin((0, 15))
D1 = Pin((0, 14))
D2 = Pin((0, 9))
D3 = Pin((0, 8))
D4 = Pin((0, 101))
D5 = Pin((0, 119))
D6 = Pin((0, 118))
D7 = Pin((0, 28))
D8 = Pin((0, 5))
D9 = Pin((0, 7))
D10 = Pin((0, 6))
D11 = Pin((0, 3))
D12 = Pin((0, 25))
D13 = Pin((0, 4))
D14 = Pin((0, 111))
D15 = Pin((0, 112))
D16 = Pin((0, 20))
D17 = Pin((0, 12))
D18 = Pin((0, 102))
D19 = Pin((0, 103))
D20 = Pin((0, 104))
D21 = Pin((0, 108))
D22 = Pin((0, 30))
D23 = Pin((0, 27))
D24 = Pin((0, 22))
D25 = Pin((0, 29))
D26 = Pin((0, 117))
D27 = Pin((0, 13))

SDA = D2
SCL = D3
MISO = D9
MOSI = D10
SCLK = D11
SCK = D11
TXD = D14
RXD = D15

spiPorts = ((1, SCLK, MOSI, MISO),)

uartPorts = ((0, TXD, RXD),)

i2cPorts = ((0, SCL, SDA),)

pwmOuts = (
    ((0, 0), D12),
    ((3, 0), D13),
)
