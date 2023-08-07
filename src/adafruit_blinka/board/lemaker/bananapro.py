# SPDX-FileCopyrightText: 2023 Xenokrates
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the LeMaker Banana Pro."""

# The LeMaker Banana Pro uses the AllWinner A20 SoC
from adafruit_blinka.microcontroller.allwinner.a20 import pin


# Pinout reference
# https://linux-sunxi.org/LeMaker_Banana_Pro#Expansion_Port

# +---------------------+Banana Pro+-----------------+
# |        Name         | Physical |       Name      |
# +---------------------+----++----+-----------------+
# |                3.3v |  1 || 2  | 5v              |
# |   PB21/TWI2_SDA/SDA |  3 || 4  | 5V              |
# |   PB20/TWI2_SCL/SCL |  5 || 6  | 0v              |
# |                 PH2 |  7 || 8  | PH4/UART4_TX/TX |
# |                  0v |  9 || 10 | PH5/UART4/RX    |
# |       PI19/UART2_RX | 11 || 12 | PI3/PWM1        |
# |       PI18/UART2_TX | 13 || 14 | 0v              |
# |                PI17 | 15 || 16 | PH20            |
# |                3.3v | 17 || 18 | PH21            |
# | PI12/SPI0_MOSI/MOSI | 19 || 20 | 0v              |
# | PI13/SPI0_MISO/SCLK | 21 || 22 | PI16            |
# |       PI11/SPI0_CLK | 23 || 24 | PI10/SPI0_CS0   |
# |                  0v | 25 || 26 | PI14/SPI0_CS1   |
# |         PI1/TW3_SDA | 27 || 28 | PI0/TWI3_SCL    |
# |                 PB3 | 29 || 30 | 0v              |
# |       PI21/UART7_RX | 31 || 32 | PI20/UART7_TX   |
# |                PB13 | 33 || 34 | 0v              |
# |                 PB7 | 35 || 36 | PB06            |
# |                 PB5 | 37 || 38 | PB12            |
# |                  0v | 39 || 40 | PB08            |
# +---------------------+----++----+-----------------+
# |        Name         | Physical |      Name       |
# +---------------------+Banana Pro+-----------------+

# 40 pin header (CON6) - Using physical pin numbering and CPU PIOs

P3 = pin.PB21
PB21 = pin.PB21
TWI2_SDA = pin.PB21
P5 = pin.PB20
PB20 = pin.PB20
TWI2_SCL = pin.PB20
P7 = pin.PH2
UART_TX = pin.PB22
PB22 = pin.PB22
UART_RX = pin.PB23
PB23 = pin.PB23
PH2 = pin.PH2
PH21 = pin.PH21
PH21 = pin.PH21
P8 = pin.PH4
PH4 = pin.PH4
UART4_RX = pin.PH4
P10 = pin.PH5
PH5 = pin.PH5
UART4_TX = pin.PH5
P11 = pin.PI19
PI19 = pin.PI19
UART2_RX = pin.PI19
P12 = pin.PI3
PWM1 = pin.PI3
PI3 = pin.PI3
P13 = pin.PI18
UART2_TX = pin.PI18
PI18 = pin.PI18
P15 = pin.PI17
PI17 = pin.PI17
P16 = pin.PH20
PH20 = pin.PH20
P18 = pin.PH21
PH21 = pin.PH21
P19 = pin.PI12
PI12 = pin.PI12
SPI0_MOSI = pin.PI12
P21 = pin.PI11
PI11 = pin.PI11
SPI0_CLK = pin.PI11
P22 = pin.PI16
PI16 = pin.PI16
P23 = pin.PI13
PI13 = pin.PI13
SPI0_MISO = pin.PI13
P24 = pin.PI10
PI10 = pin.PI10
SPI0_CS0 = pin.PI10
P26 = pin.PI14
PI14 = pin.PI14
SPI0_CS1 = pin.PI14
P27 = pin.PI1
PI1 = pin.PI1
TWI3_SDA = pin.PI1
P28 = pin.PI0
PI0 = pin.PI0
TWI3_SCL = pin.PI0
P29 = pin.PB3
PB3 = pin.PB3
P31 = pin.PI21
PI21 = pin.PI21
UART7_RX = pin.PI21
P32 = pin.PI20
PI20 = pin.PI20
UART7_TX = pin.PI20
P33 = pin.PB13
PB13 = pin.PB13
P35 = pin.PB7
PB7 = pin.PB7
P36 = pin.PB6
PB6 = pin.PB6
P37 = pin.PB5
PB5 = pin.PB5
P38 = pin.PB12
PB12 = pin.PB12
P40 = pin.PB8
PB8 = pin.PB8

## Additional Hardware

LED1 = pin.PH24
LED_GREEN = pin.PH24
LED2 = pin.PG2
LED_BLUE = pin.PG2

## For compatibility of 40-pin header to RasPi & others
## With these definitions most examples run out of the box.

D0 = pin.PI1
D1 = pin.PI0
D2 = pin.PB21
D3 = pin.PB20
D4 = pin.PH2
D5 = pin.PB3
D6 = pin.PI21
D7 = pin.PI14
D8 = pin.PI10
D9 = pin.PI13
D10 = pin.PI12
D11 = pin.PI11
D12 = pin.PI20
D13 = pin.PB13
D14 = pin.PH4
D15 = pin.PH5
D16 = pin.PB6
D17 = pin.PI19
D18 = pin.PI3
D19 = pin.PB7
D20 = pin.PB12
D21 = pin.PB8
D22 = pin.PI17
D23 = pin.PH20
D24 = pin.PH21
D25 = pin.PI16
D26 = pin.PB5
D27 = pin.PI18

RX = pin.PH4
TX = pin.PH5

SDA = pin.PB21
SCL = pin.PB20

SCLK = pin.PI11
MOSI = pin.PI12
MISO = pin.PI13
