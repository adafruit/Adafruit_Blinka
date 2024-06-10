# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
# copied from Allwinner H6 to be updated later

"""Repka Pi 4 (Allwinner H6) Pin Names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# TODO: check and update all pins after board release
PC16 = Pin((1, 79))

PD14 = Pin((1, 110))
PD15 = Pin((1, 111))
PD16 = Pin((1, 112))
PD17 = Pin((1, 113))
PD18 = Pin((1, 114))
PD19 = Pin((1, 115))
UART2_TX = PD19
PD20 = Pin((1, 116))
UART2_RX = PD20
PD21 = Pin((1, 117))
PD22 = Pin((1, 118))
PD23 = Pin((1, 119))
PD24 = Pin((1, 120))
PD25 = Pin((1, 121))
TWI0_SCL = PD25
PD26 = Pin((1, 122))
TWI0_SDA = PD26

PG10 = Pin((1, 202))
PG11 = Pin((1, 203))
PG12 = Pin((1, 204))
PG13 = Pin((1, 205))
PG14 = Pin((1, 206))

PH2 = Pin((1, 226))
PH3 = Pin((1, 227))
SPI1_CS = PH3
PH4 = Pin((1, 228))
SPI1_SCLK = PH4
PH5 = Pin((1, 229))
SPI1_MOSI = PH5
PH6 = Pin((1, 230))
SPI1_MISO = PH6
PH8 = Pin((1, 230))
PH9 = Pin((1, 231))

PL2 = Pin((0, 2))
PL3 = Pin((0, 3))
PL8 = Pin((0, 8))
PL9 = Pin((0, 9))
PL10 = Pin((0, 10))

i2cPorts = ((0, TWI0_SCL, TWI0_SDA),)
spiPorts = ((1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),)
uartPorts = ((2, UART2_TX, UART2_RX),)
