# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Allwinner A33 pin names"""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PB0 = Pin(32)  # PB0/UART2_TX/UART0_TX/PB_EINT0
UART2_TX = PB0
PB1 = Pin(33)  # PB1/UART2_RX/UART0_RX/PB_EINT1
UART2_RX = PB1

PC0 = Pin(64)  # PC0/ND_WE/SPI0_MOSI
PC1 = Pin(65)  # PC1/ND_ALE/SPI0_MISO
PC2 = Pin(66)  # PC2/ND_CLE/SPI0_CLK

PH4 = Pin(228)  # PH4/TWI1_SCK
TWI1_SCL = PH4
PH5 = Pin(229)  # PH5/TWI1_SDA
TWI1_SDA = PH5


PH6 = Pin(230)  # PH6/SPI0_CS/UART3_TX
UART3_TX = PH6
SPI0_CS = PH6

PH7 = Pin(231)  # PH7/SPI0_CLK/UART3_RX
UART3_RX = PH7
SPI0_SCLK = PH7

PH8 = Pin(232)  # PH8/SPI0_MOSI/UART3_RTS
UART3_RTS = PH8
SPI0_MOSI = PH8

PH9 = Pin(233)  # PH9/SPI0_MISO/UART3_CTS
UART3_CTS = PH9
SPI0_MISO = PH9


# ordered as i2cId, sclId, sdaId
i2cPorts = ((0, TWI1_SCL, TWI1_SDA),)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),)

# ordered as uartId, txId, rxId
uartPorts = (
    (2, UART2_TX, UART2_RX),
    (3, UART3_TX, UART3_RX),
)
