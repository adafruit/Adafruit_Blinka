# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""AmLogic s905x pin names"""
# pylint: disable=wildcard-import,unused-wildcard-import
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# Chip 0
GPIO100 = Pin((0, 0))
GPIO101 = Pin((0, 1))
GPIO104 = Pin((0, 4))
GPIO105 = Pin((0, 5))
GPIO106 = Pin((0, 6))
GPIO109 = Pin((0, 9))
GPIO110 = Pin((0, 10))

# Chip 1
GPIO220 = Pin((1, 20))
GPIO222 = Pin((1, 22))
GPIO223 = Pin((1, 23))
GPIO224 = Pin((1, 24))
GPIO225 = Pin((1, 25))
GPIO275 = Pin((1, 75))
GPIO276 = Pin((1, 76))
GPIO279 = Pin((1, 79))
GPIO280 = Pin((1, 80))
GPIO281 = Pin((1, 81))
GPIO282 = Pin((1, 82))
GPIO283 = Pin((1, 83))
GPIO284 = Pin((1, 84))
GPIO285 = Pin((1, 85))
GPIO286 = Pin((1, 86))
GPIO287 = Pin((1, 87))
GPIO288 = Pin((1, 88))
GPIO289 = Pin((1, 89))
GPIO290 = Pin((1, 90))
GPIO291 = Pin((1, 91))
GPIO292 = Pin((1, 92))
GPIO293 = Pin((1, 93))
GPIO294 = Pin((1, 94))
GPIO295 = Pin((1, 95))
GPIO296 = Pin((1, 96))
GPIO297 = Pin((1, 97))
GPIO298 = Pin((1, 98))

I2C0_SDA = GPIO105
I2C0_SCK = GPIO104
I2C1_SDA = GPIO275
I2C1_SCK = GPIO276

UART1_RX = GPIO288
UART1_TX = GPIO287
UART2_RX = GPIO292
UART2_TX = GPIO291

SPI0_SCLK = GPIO290
SPI0_MISO = GPIO288
SPI0_MOSI = GPIO287
SPI0_CS = GPIO289
SPI1_SCLK = GPIO223
SPI1_MISO = GPIO288
SPI1_MOSI = GPIO287
SPI1_CS = GPIO289

i2cPorts = (
    (0, I2C0_SCK, I2C0_SDA),
    (1, I2C1_SCK, I2C1_SDA),
)

spiPorts = ((0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO), (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO))

uartPorts = (
    (1, UART1_TX, UART1_RX),
    (2, UART2_TX, UART2_RX),
)
