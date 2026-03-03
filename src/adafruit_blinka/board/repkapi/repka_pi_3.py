# SPDX-FileCopyrightText: 2024 Suren Khorenyan
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Repka Pi 3"""
from adafruit_blinka.microcontroller.allwinner.h5 import pin

PA0 = pin.PA0
UART2_TX = pin.UART2_TX
PA1 = pin.PA1
UART2_RX = pin.UART2_RX
PA2 = pin.PA2
PA3 = pin.PA3
SPI0_CS1 = pin.SPI0_CS1
PA4 = pin.PA4
UART0_TX = pin.UART0_TX
PA5 = pin.PA5
UART0_RX = pin.UART0_RX
PA6 = pin.PA6
PA7 = pin.PA7
PA8 = pin.PA8
PA9 = pin.PA9
PA10 = pin.PA10
PA11 = pin.PA11
TWI1_SCL = pin.TWI1_SCL
PA12 = pin.PA12
TWI1_SDA = pin.TWI1_SDA
PA13 = pin.PA13
SPI1_CS0 = pin.SPI1_CS0
PA14 = pin.PA14
SPI1_CLK = pin.SPI1_SCLK
PA15 = pin.PA15
SPI1_MOSI = pin.SPI1_MOSI
PA16 = pin.PA16
SPI1_MISO = pin.SPI1_MISO
PA18 = pin.PA18
TWI2_SCL = pin.PA18
PA19 = pin.PA19
TWI2_SDA = pin.PA19
PA21 = pin.PA21

PC0 = pin.PC0
SPI0_MOSI = pin.SPI0_MOSI
PC1 = pin.PC1
SPI0_MISO = pin.SPI0_MISO
PC2 = pin.PC2
SPI0_CLK = pin.SPI0_SCLK
PC3 = pin.PC3
SPI0_CS0 = pin.SPI0_CS

PL2 = pin.PL2
S_UART_TX = pin.S_UART_TX
PL3 = pin.PL3
S_UART_RX = pin.S_UART_RX
PL11 = pin.PL11

# default I2C
SCL = TWI1_SCL
SDA = TWI1_SDA
