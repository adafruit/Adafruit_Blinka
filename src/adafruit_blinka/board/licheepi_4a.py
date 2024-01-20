# SPDX-FileCopyrightText: 2024 Chris Brown
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Lichee Pi 4A."""

from adafruit_blinka.microcontroller.thead.th1520 import pin

IO1_6 = pin.GPIO1_6
IO1_5 = pin.GPIO1_5
IO1_4 = pin.GPIO1_4
IO1_3 = pin.GPIO1_3
I2C2_SCL = pin.TWI2_SCL
U2_TX = pin.UART2_TX
I2C2_SDA = pin.TWI2_SDA
U2_RX = pin.UART2_RX
U3_TX = pin.UART3_TX
U3_RX = pin.UART3_RX
U1_TX = pin.UART1_TX
U1_RX = pin.UART1_RX
U0_TX = pin.UART0_TX
U0_RX = pin.UART0_RX
QSPI1_SO = pin.SPI1_MISO
QSPI1_CS = pin.SPI1_CS
QSPI1_SI = pin.SPI1_MOSI
QSPI1_CLK = pin.SPI1_SCLK

# Default UART
TX = U0_TX
RX = U0_RX

# Default I2C
SCL = I2C2_SCL
SDA = I2C2_SDA

# Default SPI
SCLK = QSPI1_CLK
MOSI = QSPI1_SI
MISO = QSPI1_SO
CS = QSPI1_CS
