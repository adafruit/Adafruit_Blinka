# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Orange Pi Zero."""

# The Orange Pi Zero uses the AllWinner H2 SoC, but pins
# are the same as the AllWinner H3 SoC, so we import those
from adafruit_blinka.microcontroller.allwinner.h3 import pin

PA12 = pin.PA12
SDA = pin.PA12
PA11 = pin.PA11
SCL = pin.PA11
PA6 = pin.PA6
PWM1 = pin.PA6
PA1 = pin.PA1
UART2_RX = pin.PA1
PA0 = pin.PA0
UART2_TX = pin.PA0
PA3 = pin.PA3
UART2_CTS = pin.PA3
PA10 = pin.PA10

PA13 = pin.PA13
SPI1_CS = pin.PA13
PA14 = pin.PA14
SPI1_CLK = pin.PA14
PA2 = pin.PA2
UART2_RTS = pin.PA2
PA18 = pin.PA18
TWI1_SCK = pin.PA18
PG6 = pin.PG6
UART1_TX = pin.PG6
PG7 = pin.PG7
UART1_RX = pin.PG7

SCLK = pin.PA14
MOSI = pin.PA15
MISO = pin.PA16
