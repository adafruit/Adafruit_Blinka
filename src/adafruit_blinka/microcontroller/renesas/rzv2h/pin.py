# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Renesas RZV2H Pin Names"""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

P0_0 = Pin((0, 0))
P0_1 = Pin((0, 1))
P0_2 = Pin((0, 2))
P0_3 = Pin((0, 3))
P0_4 = Pin((0, 4))
P0_5 = Pin((0, 5))
P0_6 = Pin((0, 6))
P0_7 = Pin((0, 7))

P1_0 = Pin((0, 8))
P1_1 = Pin((0, 9))
P1_2 = Pin((0, 10))
P1_3 = Pin((0, 11))
P1_4 = Pin((0, 12))
P1_5 = Pin((0, 13))
P1_6 = Pin((0, 14))
P1_7 = Pin((0, 15))

P2_0 = Pin((0, 16))
P2_1 = Pin((0, 17))
P2_2 = Pin((0, 18))
P2_3 = Pin((0, 19))
P2_4 = Pin((0, 20))
P2_5 = Pin((0, 21))
P2_6 = Pin((0, 22))
P2_7 = Pin((0, 23))

P3_0 = Pin((0, 24))
P3_1 = Pin((0, 25))
P3_2 = Pin((0, 26))
P3_3 = Pin((0, 27))
P3_4 = Pin((0, 28))
P3_5 = Pin((0, 29))
P3_6 = Pin((0, 30))
P3_7 = Pin((0, 31))

P4_0 = Pin((0, 32))
P4_1 = Pin((0, 33))
P4_2 = Pin((0, 34))
P4_3 = Pin((0, 35))
P4_4 = Pin((0, 36))
P4_5 = Pin((0, 37))
P4_6 = Pin((0, 38))
P4_7 = Pin((0, 39))

P5_0 = Pin((0, 40))
P5_1 = Pin((0, 41))
P5_2 = Pin((0, 42))
P5_3 = Pin((0, 43))
P5_4 = Pin((0, 44))
P5_5 = Pin((0, 45))
P5_6 = Pin((0, 46))
P5_7 = Pin((0, 47))

P6_0 = Pin((0, 48))
P6_1 = Pin((0, 49))
P6_2 = Pin((0, 50))
P6_3 = Pin((0, 51))
P6_4 = Pin((0, 52))
P6_5 = Pin((0, 53))
P6_6 = Pin((0, 54))
P6_7 = Pin((0, 55))

P7_0 = Pin((0, 56))
P7_1 = Pin((0, 57))
P7_2 = Pin((0, 58))
P7_3 = Pin((0, 59))
P7_4 = Pin((0, 60))
P7_5 = Pin((0, 61))
P7_6 = Pin((0, 62))
P7_7 = Pin((0, 63))

P8_0 = Pin((0, 64))
P8_1 = Pin((0, 65))
P8_2 = Pin((0, 66))
P8_3 = Pin((0, 67))
P8_4 = Pin((0, 68))
P8_5 = Pin((0, 69))
P8_6 = Pin((0, 70))
P8_7 = Pin((0, 71))

P9_0 = Pin((0, 72))
P9_1 = Pin((0, 73))
P9_2 = Pin((0, 74))
P9_3 = Pin((0, 75))
P9_4 = Pin((0, 76))
P9_5 = Pin((0, 77))
P9_6 = Pin((0, 78))
P9_7 = Pin((0, 79))

PA_0 = Pin((0, 80))
PA_1 = Pin((0, 81))
PA_2 = Pin((0, 82))
PA_3 = Pin((0, 83))
PA_4 = Pin((0, 84))
PA_5 = Pin((0, 85))
PA_6 = Pin((0, 86))
PA_7 = Pin((0, 87))

PB_0 = Pin((0, 88))
PB_1 = Pin((0, 89))
PB_2 = Pin((0, 90))
PB_3 = Pin((0, 91))
PB_4 = Pin((0, 92))
PB_5 = Pin((0, 93))
PB_6 = Pin((0, 94))
PB_7 = Pin((0, 95))

# I2C
I2C0_SCL = P3_1
I2C0_SDA = P3_0
I2C1_SCL = P3_3
I2C1_SDA = P3_2
I2C2_SCL = P2_1
I2C2_SDA = P2_0
I2C3_SCL = P3_7
I2C3_SDA = P3_6
I2C4_SCL = P4_1
I2C4_SDA = P4_0
I2C5_SCL = P4_3
I2C5_SDA = P4_2
I2C6_SCL = P4_5
I2C6_SDA = P4_4
I2C7_SCL = P4_7
I2C7_SDA = P4_6
I2C8_SCL = P0_7
I2C8_SDA = P0_6

i2cPorts = (
    (0, I2C0_SCL, I2C0_SDA),
    (1, I2C1_SCL, I2C1_SDA),
    (2, I2C2_SCL, I2C2_SDA),
    (3, I2C3_SCL, I2C3_SDA),
    (4, I2C4_SCL, I2C4_SDA),
    (5, I2C5_SCL, I2C5_SDA),
    (6, I2C6_SCL, I2C6_SDA),
    (7, I2C7_SCL, I2C7_SDA),
    (8, I2C8_SCL, I2C8_SDA),
)

# SPI
SPI0_MOSI = P9_0
SPI0_MISO = P9_1
SPI0_SCLK = P9_2
SPI0_CS0 = P9_3
SPI1_MOSI = PB_1
SPI1_MISO = PB_2
SPI1_SCLK = PB_0
SPI1_CS0 = P3_4
SPI2_MOSI = PB_4
SPI2_MISO = PB_3
SPI2_SCLK = PB_5
SPI2_CS0 = PA_7

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),
    (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),
    (2, SPI2_SCLK, SPI2_MOSI, SPI2_MISO),
)

# UART
UART0_TX = P5_0
UART0_RX = P5_1
# UART1_TX = P5_2
# UART1_RX = P5_3
UART2_TX = P5_4
UART2_RX = P5_5
UART3_TX = P3_4
UART3_RX = P4_5
UART4_TX = P4_0
UART4_RX = P4_1
UART5_TX = P4_4
UART5_RX = P4_5
UART6_TX = P9_0
UART6_RX = P9_1
UART7_TX = P9_4
UART7_RX = P9_5
UART8_TX = PB_1
UART8_RX = PB_2
UART9_TX = PB_4
UART9_RX = PB_3

# ordered as uartId, txId, rxId
# uart0 map to /dev/ttySC1
uartPorts = (
    (0, UART0_TX, UART0_RX),
    # (1, UART1_TX, UART1_RX),
    (2, UART2_TX, UART2_RX),
    (3, UART3_TX, UART3_RX),
    (4, UART4_TX, UART4_RX),
    (5, UART5_TX, UART5_RX),
    (6, UART6_TX, UART6_RX),
    (7, UART7_TX, UART7_RX),
    (8, UART8_TX, UART8_RX),
    (9, UART9_TX, UART9_RX),
)

# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = []
