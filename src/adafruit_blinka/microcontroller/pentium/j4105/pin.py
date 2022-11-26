# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Intel Celeron j4105 pin names"""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

GPIO388 = Pin((1,36))
GPIO389 = Pin((1,37))
GPIO386 = Pin((1,34))
GPIO387 = Pin((1,35))
GPIO337 = Pin((2,5))
GPIO415 = Pin((1,63))
GPIO416 = Pin((1,64))
GPIO357 = Pin((1,5))
GPIO356 = Pin((1,4))
GPIO358 = Pin((1,6))
GPIO359 = Pin((1,7))
GPIO355 = Pin((1,3))
GPIO391 = Pin((1,39))
GPIO417 = Pin((1,65))
GPIO493 = Pin((0,61))
GPIO492 = Pin((0,60))
GPIO410 = Pin((1,58))
GPIO364 = Pin((1,12))
GPIO338 = Pin((2,6))
GPIO339 = Pin((2,7))
GPIO340 = Pin((2,8))
GPIO341 = Pin((2,9))
GPIO413 = Pin((1,61))
GPIO421 = Pin((1,69))
GPIO422 = Pin((1,70))
GPIO390 = Pin((1,38))
GPIO419 = Pin((1,67))
GPIO412 = Pin((1,60))

SPI0_SCLK = GPIO355
SPI0_MOSI = GPIO359
SPI0_MISO = GPIO358
SPI0_FSO = GPIO356
SPI0_FS1 = GPIO357

UART0_TX = GPIO493
UART0_RX = GPIO492

I2C5_SDA = GPIO386
I2C5_SCL = GPIO387

I2C6_SDA = GPIO388
I2C6_SCL = GPIO389

i2cPorts = ((2, I2C5_SCL, I2C5_SDA),(3, I2C6_SCL, I2C6_SDA),)
# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),)
# ordered as uartId, txId, rxId
uartPorts = ((0, UART0_TX, UART0_RX),)
