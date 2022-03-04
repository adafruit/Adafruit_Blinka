# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""A Pin class for use with StarFive JH71x0."""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

D0 = Pin(9)
D1 = Pin(10)
D4 = Pin(46)
D5 = Pin(8)
D6 = Pin(6)
D7 = Pin(11)
D8 = Pin(15)
D9 = Pin(16)
D10 = Pin(18)
D11 = Pin(12)
D12 = Pin(7)
D13 = Pin(5)
D14 = Pin(14)
D15 = Pin(13)
D16 = Pin(4)
D17 = Pin(44)
D18 = Pin(45)
D19 = Pin(3)
D20 = Pin(2)
D21 = Pin(0)
D22 = Pin(20)
D23 = Pin(21)
D24 = Pin(19)
D25 = Pin(17)
D26 = Pin(1)
D27 = Pin(22)

# I2C
I2C1_SDA = Pin(48)
I2C1_SCL = Pin(47)
I2C2_SDA = Pin(59)
I2C2_SCL = Pin(60)
I2C3_SDA = Pin(61)
I2C3_SCL = Pin(62)

# SPI
SPI_MISO = D9
SPI_MOSI = D10
SPI_SCLK = D11

# UART
UART_TX = D14
UART_RX = D15

# ordered as i2cId, SCL, SDA
i2cPorts = (
    (0, I2C1_SCL, I2C1_SDA),
    (1, I2C2_SCL, I2C2_SDA),
    (2, I2C3_SCL, I2C3_SDA),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI_SCLK, SPI_MOSI, SPI_MISO),)
