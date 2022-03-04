# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Allwinner H3 pin names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PA0 = Pin(0)
UART2_TX = PA0
PA1 = Pin(1)
UART2_RX = PA1
PA2 = Pin(2)
PA3 = Pin(3)
PA6 = Pin(6)
PA7 = Pin(7)
PA8 = Pin(8)
PA9 = Pin(9)
PA10 = Pin(10)
PA11 = Pin(11)
TWI0_SCL = PA11
PA12 = Pin(12)
TWI0_SDA = PA12
PA13 = Pin(13)
UART3_TX = PA13
PA14 = Pin(14)
UART3_RX = PA14
SPI1_SCLK = PA14
PA15 = Pin(15)
SPI1_MOSI = PA15
PA16 = Pin(16)
SPI1_MISO = PA16
PA17 = Pin(17)
PA18 = Pin(18)
PA19 = Pin(19)
PA20 = Pin(20)
PA21 = Pin(21)

PC0 = Pin(64)
SPI0_MOSI = PC0
PC1 = Pin(65)
SPI0_MISO = PC1
PC2 = Pin(66)
SPI0_SCLK = PC2
PC3 = Pin(67)
SPI0_CS = PC3
PC4 = Pin(68)
PC7 = Pin(71)

PD14 = Pin(110)

PG6 = Pin(198)
UART1_TX = PG6
PG7 = Pin(199)
UART1_RX = PG7
PG8 = Pin(200)
PG9 = Pin(201)
PG10 = Pin(202)
PG11 = Pin(203)
PG12 = Pin(204)
PG13 = Pin(205)

PL2 = Pin((1, 2))
PL4 = Pin((1, 4))

i2cPorts = ((0, TWI0_SCL, TWI0_SDA),)
# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),
    (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),
)
# ordered as uartId, txId, rxId
uartPorts = ((3, UART3_TX, UART3_RX),)
