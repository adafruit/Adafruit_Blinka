# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Allwinner H5 pin names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PA0 = Pin((1, 0))
UART2_TX = PA0
PA1 = Pin((1, 1))
UART2_RX = PA1
PA2 = Pin((1, 2))
PA3 = Pin((1, 3))
PA6 = Pin((1, 6))
PA7 = Pin((1, 7))
PA8 = Pin((1, 8))
PA9 = Pin((1, 9))
PA10 = Pin((1, 10))
PA11 = Pin((1, 11))
TWI0_SCL = PA11
PA12 = Pin((1, 12))
TWI0_SDA = PA12
PA13 = Pin((1, 13))
UART3_TX = PA13
PA14 = Pin((1, 14))
UART3_RX = PA14
SPI1_SCLK = PA14
PA15 = Pin((1, 15))
SPI1_MOSI = PA15
PA16 = Pin((1, 16))
SPI1_MISO = PA16
PA17 = Pin((1, 17))
PA18 = Pin((1, 18))
PA19 = Pin((1, 19))
PA20 = Pin((1, 20))
PA21 = Pin((1, 21))

PC0 = Pin((1, 64))
SPI0_MOSI = PC0
PC1 = Pin((1, 65))
SPI0_MISO = PC1
PC2 = Pin((1, 66))
SPI0_SCLK = PC2
PC3 = Pin((1, 67))
SPI0_CS = PC3
PC4 = Pin((1, 68))
PC5 = Pin((1, 69))
PC6 = Pin((1, 70))
PC7 = Pin((1, 71))

PD11 = Pin((1, 107))
PD14 = Pin((1, 110))

PG6 = Pin((1, 198))
UART1_TX = PG6
PG7 = Pin((1, 199))
UART1_RX = PG7
PG8 = Pin((1, 200))
PG9 = Pin((1, 201))
PG10 = Pin((1, 202))
PG11 = Pin((1, 203))
PG12 = Pin((1, 204))
PG13 = Pin((1, 205))

PL0 = Pin((0, 0))
PL1 = Pin((0, 1))

i2cPorts = ((0, TWI0_SCL, TWI0_SDA),)
# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),
    (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),
)
# ordered as uartId, txId, rxId
uartPorts = ((3, UART3_TX, UART3_RX),)
