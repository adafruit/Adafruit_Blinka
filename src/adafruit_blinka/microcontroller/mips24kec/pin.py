# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""MIPS 24kec pin names"""
from adafruit_blinka.microcontroller.generic_linux.periphery_pin import Pin

GPIO0 = Pin(0)
GPIO1 = Pin(1)
GPIO2 = Pin(2)
GPIO3 = Pin(3)
GPIO4 = Pin(4)  # I2C SDA
GPIO5 = Pin(5)  # I2C SCL
GPIO6 = Pin(6)  # SPI CS
GPIO7 = Pin(7)  # SPI SCLK
GPIO8 = Pin(8)  # SPI MOSI
GPIO9 = Pin(9)  # SPI MISO
GPIO10 = Pin(10)

GPIO11 = Pin(11)
GPIO12 = Pin(12)
GPIO13 = Pin(13)
GPIO14 = Pin(14)
GPIO15 = Pin(15)
GPIO16 = Pin(16)
GPIO17 = Pin(17)

GPIO18 = Pin(18)
GPIO19 = Pin(19)

GPIO20 = Pin(20)
GPIO21 = Pin(21)
GPIO22 = Pin(22)
GPIO23 = Pin(23)

GPIO37 = Pin((1, 5))
GPIO38 = Pin((1, 6))
GPIO43 = Pin((1, 11))
GPIO44 = Pin((1, 12))
GPIO45 = Pin((1, 13))
GPIO46 = Pin((1, 14))

UART0_TX = GPIO12
UART0_RX = GPIO13

UART1_TX = GPIO45
UART1_RX = GPIO46

UART2_TX = GPIO20
UART2_RX = GPIO21

SPI0_MOSI = GPIO8
SPI0_MISO = GPIO9
SPI0_SCLK = GPIO7
SPI0_CS = GPIO6

I2C0_SDA = GPIO4
I2C0_SCL = GPIO5

# ordered as i2cId, sclId, sdaId
i2cPorts = ((0, I2C0_SCL, I2C0_SDA),)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (((0, 1), SPI0_SCLK, SPI0_MOSI, SPI0_MISO),)

# ordered as uartId, txId, rxId
uartPorts = (
    (0, UART0_TX, UART0_RX),
    (1, UART1_TX, UART1_RX),
)
