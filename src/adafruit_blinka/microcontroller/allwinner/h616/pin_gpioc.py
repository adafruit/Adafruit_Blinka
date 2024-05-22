# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Allwinner H616 Pin Names"""

try:
    import gpioc
except ImportError:
    raise ImportError(
        "gpioc Python bindings not found, please install and try again! See "
        "https://pypi.org/project/gpioc/"
        "\n you can run 'pip install gpioc'"
    ) from ImportError

from gpioc.pin import Pin

PC0 = Pin(64)
SPI0_SCLK = PC0
PC1 = Pin(65)
PC2 = Pin(66)
SPI0_MOSI = PC2
PC3 = Pin(67)
SPI0_CS0 = PC3
PC4 = Pin(68)
SPI0_MISO = PC4
PC5 = Pin(69)
PC6 = Pin(70)
PC7 = Pin(71)
PC8 = Pin(72)
PC9 = Pin(73)
PC10 = Pin(74)
PC11 = Pin(75)
PC12 = Pin(76)
PC13 = Pin(77)
PC14 = Pin(78)
PC15 = Pin(79)

PF0 = Pin(160)
PF1 = Pin(161)
PF2 = Pin(162)
PF3 = Pin(163)
PF4 = Pin(164)
PF5 = Pin(165)
PF6 = Pin(166)

PG0 = Pin(192)
PG1 = Pin(193)
PG2 = Pin(194)
PG3 = Pin(195)
PG4 = Pin(196)
PG5 = Pin(197)
PG6 = Pin(198)
PG7 = Pin(199)
PG8 = Pin(200)
PG9 = Pin(201)
PG10 = Pin(202)
PG11 = Pin(203)
PG12 = Pin(204)
PG13 = Pin(205)
PG14 = Pin(206)
PG15 = Pin(207)
PG16 = Pin(208)
PG17 = Pin(209)
PG18 = Pin(210)
PG19 = Pin(211)

PH0 = Pin(224)
PH1 = Pin(225)
PH2 = Pin(226)
UART5_TX = PH2
PH3 = Pin(227)
UART5_RX = PH3
PH4 = Pin(228)
TWI3_SCL = PH4
PH5 = Pin(229)
UART2_TX = PH5
TWI3_SDA = PH5
SPI1_CS0 = PH5
PH6 = Pin(230)
UART2_RX = PH6
SPI1_SCLK = PH6
PH7 = Pin(231)
SPI1_MOSI = PH7
PH8 = Pin(232)
SPI1_MISO = PH8
PH9 = Pin(233)
SPI1_CS1 = PH9
PH10 = Pin(234)

PI0 = Pin(256)
PI1 = Pin(257)
PI2 = Pin(258)
PI3 = Pin(259)
PI4 = Pin(260)
PI5 = Pin(261)
PI6 = Pin(262)
PI7 = Pin(263)
TWI1_SCL = PI7
PI8 = Pin(264)
TWI1_SDA = PI8
PI9 = Pin(265)
TWI2_SCL = PI9
PI10 = Pin(266)
TWI2_SDA = PI10
PI11 = Pin(267)
PI12 = Pin(268)
PI13 = Pin(269)
UART4_TX = PI13
PI14 = Pin(270)
UART4_RX = PI14
PI15 = Pin(271)
PI16 = Pin(272)

i2cPorts = (
    (1, TWI1_SCL, TWI1_SDA),
    (2, TWI2_SCL, TWI2_SDA),
    (3, TWI3_SCL, TWI3_SDA),
)
# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),
    (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),
)
# ordered as uartId, txId, rxId
uartPorts = (
    (2, UART2_TX, UART2_RX),
    (4, UART4_TX, UART4_RX),
    (5, UART5_TX, UART5_RX),
)
