# SPDX-FileCopyrightText: 2024 Suren Khorenyan
#
# SPDX-License-Identifier: MIT
"""Repka Pi 3 (Allwinner H5) pin names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PA0 = Pin((1, 0))
UART2_TX = PA0
PA1 = Pin((1, 1))
UART2_RX = PA1
PA2 = Pin((1, 2))
PA3 = Pin((1, 3))
SPI0_CS1 = PA3
PA4 = Pin((1, 4))
UART0_TX = PA4
PA5 = Pin((1, 5))
UART0_RX = PA5
PA6 = Pin((1, 6))
PA7 = Pin((1, 7))
PA8 = Pin((1, 8))
PA9 = Pin((1, 9))
PA10 = Pin((1, 10))
PA11 = Pin((1, 11))
TWI1_SCL = PA11
PA12 = Pin((1, 12))
TWI1_SDA = PA12
PA13 = Pin((1, 13))
SPI1_CS0 = PA13
PA14 = Pin((1, 14))
SPI1_CLK = PA14
PA15 = Pin((1, 15))
SPI1_MOSI = PA15
PA16 = Pin((1, 16))
SPI1_MISO = PA16
PA18 = Pin((1, 18))
TWI2_SCL = PA18
PA19 = Pin((1, 19))
TWI2_SDA = PA19
PA21 = Pin((1, 21))

PC0 = Pin((1, 64))
SPI0_MOSI = PC0
PC1 = Pin((1, 65))
SPI0_MISO = PC1
PC2 = Pin((1, 66))
SPI0_CLK = PC2
PC3 = Pin((1, 67))
SPI0_CS0 = PC3


PL2 = Pin((1, 354))
S_UART_TX = PL2
PL3 = Pin((1, 355))
S_UART_RX = PL3
PL11 = Pin((1, 363))


i2cPorts = (
    (1, TWI1_SCL, TWI1_SDA),
    # todo: check pinout in `/proc/device-tree/repka-pinout`?
    (2, TWI2_SCL, TWI2_SDA),
)
# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SPI0_CLK, SPI0_MOSI, SPI0_MISO),
    (1, SPI1_CLK, SPI1_MOSI, SPI1_MISO),
)
# ordered as uartId, txId, rxId
uartPorts = (
    # todo: check uart ids
    (0, UART0_TX, UART0_RX),
    (2, UART2_TX, UART2_RX),
    (1, S_UART_TX, S_UART_RX),
)


# default I2C
SCL = i2cPorts[0][1]
SDA = i2cPorts[0][2]
