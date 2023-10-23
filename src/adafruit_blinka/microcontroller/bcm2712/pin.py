# SPDX-FileCopyrightText: 2023 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Broadcom BCM2712 pin names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# Pi 1B rev1 only?
D0 = Pin((4, 0))
D1 = Pin((4, 1))

D2 = Pin((4, 2))
SDA = Pin((4, 2))
D3 = Pin((4, 3))
SCL = Pin((4, 3))

D4 = Pin((4, 4))
D5 = Pin((4, 5))
D6 = Pin((4, 6))

D7 = Pin((4, 7))
CE1 = Pin((4, 7))
D8 = Pin((4, 8))
CE0 = Pin((4, 8))
D9 = Pin((4, 9))
MISO = Pin((4, 9))
D10 = Pin((4, 10))
MOSI = Pin((4, 10))
D11 = Pin((4, 11))
SCLK = Pin((4, 11))  # Raspberry Pi naming
SCK = Pin((4, 11))  # CircuitPython naming

D12 = Pin((4, 12))
D13 = Pin((4, 13))

D14 = Pin((4, 14))
TXD = Pin((4, 14))
D15 = Pin((4, 15))
RXD = Pin((4, 15))

D16 = Pin((4, 16))
D17 = Pin((4, 17))
D18 = Pin((4, 18))
D19 = Pin((4, 19))
MISO_1 = Pin((4, 19))
D20 = Pin((4, 20))
MOSI_1 = Pin((4, 20))
D21 = Pin((4, 21))
SCLK_1 = Pin((4, 21))
SCK_1 = Pin((4, 21))
D22 = Pin((4, 22))
D23 = Pin((4, 23))
D24 = Pin((4, 24))
D25 = Pin((4, 25))
D26 = Pin((4, 26))
D27 = Pin((4, 27))
D28 = Pin((4, 28))
D29 = Pin((4, 29))
D30 = Pin((4, 30))
D31 = Pin((4, 31))
D32 = Pin((4, 32))
D33 = Pin((4, 33))
D34 = Pin((4, 34))
D35 = Pin((4, 35))
D36 = Pin((4, 36))
D37 = Pin((4, 37))
D38 = Pin((4, 38))
D39 = Pin((4, 39))
D40 = Pin((4, 40))
MISO_2 = Pin((4, 40))
D41 = Pin((4, 41))
MOSI_2 = Pin((4, 41))
D42 = Pin((4, 42))
SCLK_2 = Pin((4, 42))
SCK_2 = Pin((4, 43))
D43 = Pin((4, 43))
D44 = Pin((4, 44))
D45 = Pin((4, 45))

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SCLK, MOSI, MISO),
    (1, SCLK_1, MOSI_1, MISO_1),
    (2, SCLK_2, MOSI_2, MISO_2),
)

# ordered as uartId, txId, rxId
uartPorts = ((1, TXD, RXD),)

# These are the known hardware I2C ports / pins.
# For software I2C ports created with the i2c-gpio overlay, see:
#     https://github.com/adafruit/Adafruit_Python_Extended_Bus
i2cPorts = (
    (1, SCL, SDA),
    (0, D1, D0),  # both pi 1 and pi 2 i2c ports!
)
