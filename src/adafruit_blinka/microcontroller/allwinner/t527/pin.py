# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Allwinner T527 Pin Names"""
import gpiod
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

chip0 = gpiod.Chip("/dev/gpiochip0")
chip1 = gpiod.Chip("/dev/gpiochip1")
num = chip0.get_info().num_lines

if num < 100:
    __chip_num = 1
    __chip_r_num = 0
else:
    __chip_num = 0
    __chip_r_num = 1

chip0.close()
chip1.close()

PB0 = Pin((__chip_num, 32))
PB1 = Pin((__chip_num, 33))
PB2 = Pin((__chip_num, 34))
PB3 = Pin((__chip_num, 35))
PB4 = Pin((__chip_num, 36))
PB5 = Pin((__chip_num, 37))
PB6 = Pin((__chip_num, 38))
PB7 = Pin((__chip_num, 39))
PB8 = Pin((__chip_num, 40))
PB9 = Pin((__chip_num, 41))
PB10 = Pin((__chip_num, 42))
PB11 = Pin((__chip_num, 43))
PB12 = Pin((__chip_num, 44))
PB13 = Pin((__chip_num, 45))
PB14 = Pin((__chip_num, 46))

PC0 = Pin((__chip_num, 64))
PC1 = Pin((__chip_num, 65))
PC2 = Pin((__chip_num, 66))
PC3 = Pin((__chip_num, 67))
PC4 = Pin((__chip_num, 68))
PC5 = Pin((__chip_num, 69))
PC6 = Pin((__chip_num, 70))
PC7 = Pin((__chip_num, 71))
PC8 = Pin((__chip_num, 72))
PC9 = Pin((__chip_num, 73))
PC10 = Pin((__chip_num, 74))
PC11 = Pin((__chip_num, 75))
PC12 = Pin((__chip_num, 76))
PC13 = Pin((__chip_num, 77))
PC14 = Pin((__chip_num, 78))
PC15 = Pin((__chip_num, 79))
PC16 = Pin((__chip_num, 80))

PD0 = Pin((__chip_num, 96))
PD1 = Pin((__chip_num, 97))
PD2 = Pin((__chip_num, 98))
PD3 = Pin((__chip_num, 99))
PD4 = Pin((__chip_num, 100))
PD5 = Pin((__chip_num, 101))
PD6 = Pin((__chip_num, 102))
PD7 = Pin((__chip_num, 103))
PD8 = Pin((__chip_num, 104))
PD9 = Pin((__chip_num, 105))
PD10 = Pin((__chip_num, 106))
PD11 = Pin((__chip_num, 107))
PD12 = Pin((__chip_num, 108))
PD13 = Pin((__chip_num, 109))
PD14 = Pin((__chip_num, 110))
PD15 = Pin((__chip_num, 111))
PD16 = Pin((__chip_num, 112))
PD17 = Pin((__chip_num, 113))
PD18 = Pin((__chip_num, 114))
PD19 = Pin((__chip_num, 115))
PD20 = Pin((__chip_num, 116))
PD21 = Pin((__chip_num, 117))
PD22 = Pin((__chip_num, 118))
PD23 = Pin((__chip_num, 119))

PE0 = Pin((__chip_num, 128))
PE1 = Pin((__chip_num, 129))
PE2 = Pin((__chip_num, 130))
PE3 = Pin((__chip_num, 131))
PE4 = Pin((__chip_num, 132))
PE5 = Pin((__chip_num, 133))
PE6 = Pin((__chip_num, 134))
PE7 = Pin((__chip_num, 135))
PE8 = Pin((__chip_num, 136))
PE9 = Pin((__chip_num, 137))
PE10 = Pin((__chip_num, 138))
PE11 = Pin((__chip_num, 139))
PE12 = Pin((__chip_num, 140))
PE13 = Pin((__chip_num, 141))
PE14 = Pin((__chip_num, 142))
PE15 = Pin((__chip_num, 143))

PF0 = Pin((__chip_num, 160))
PF1 = Pin((__chip_num, 161))
PF2 = Pin((__chip_num, 162))
PF3 = Pin((__chip_num, 163))
PF4 = Pin((__chip_num, 164))
PF5 = Pin((__chip_num, 165))
PF6 = Pin((__chip_num, 166))

PG0 = Pin((__chip_num, 192))
PG1 = Pin((__chip_num, 193))
PG2 = Pin((__chip_num, 194))
PG3 = Pin((__chip_num, 195))
PG4 = Pin((__chip_num, 196))
PG5 = Pin((__chip_num, 197))
PG6 = Pin((__chip_num, 198))
PG7 = Pin((__chip_num, 199))
PG8 = Pin((__chip_num, 200))
PG9 = Pin((__chip_num, 201))
PG10 = Pin((__chip_num, 202))
PG11 = Pin((__chip_num, 203))
PG12 = Pin((__chip_num, 204))
PG13 = Pin((__chip_num, 205))
PG14 = Pin((__chip_num, 206))

PH0 = Pin((__chip_num, 224))
PH1 = Pin((__chip_num, 225))
PH2 = Pin((__chip_num, 226))
PH3 = Pin((__chip_num, 227))
PH4 = Pin((__chip_num, 228))
PH5 = Pin((__chip_num, 229))
PH6 = Pin((__chip_num, 230))
PH7 = Pin((__chip_num, 231))
PH8 = Pin((__chip_num, 232))
PH9 = Pin((__chip_num, 233))
PH10 = Pin((__chip_num, 234))
PH11 = Pin((__chip_num, 235))
PH12 = Pin((__chip_num, 236))
PH13 = Pin((__chip_num, 237))
PH14 = Pin((__chip_num, 238))
PH15 = Pin((__chip_num, 239))
PH16 = Pin((__chip_num, 240))
PH17 = Pin((__chip_num, 241))
PH18 = Pin((__chip_num, 242))
PH19 = Pin((__chip_num, 243))

PI0 = Pin((__chip_num, 256))
PI1 = Pin((__chip_num, 257))
PI2 = Pin((__chip_num, 258))
PI3 = Pin((__chip_num, 259))
PI4 = Pin((__chip_num, 260))
PI5 = Pin((__chip_num, 261))
PI6 = Pin((__chip_num, 262))
PI7 = Pin((__chip_num, 263))
PI8 = Pin((__chip_num, 264))
PI9 = Pin((__chip_num, 265))
PI10 = Pin((__chip_num, 266))
PI11 = Pin((__chip_num, 267))
PI12 = Pin((__chip_num, 268))
PI13 = Pin((__chip_num, 269))
PI14 = Pin((__chip_num, 270))
PI15 = Pin((__chip_num, 271))
PI16 = Pin((__chip_num, 272))

PJ0 = Pin((__chip_num, 288))
PJ1 = Pin((__chip_num, 289))
PJ2 = Pin((__chip_num, 290))
PJ3 = Pin((__chip_num, 291))
PJ4 = Pin((__chip_num, 292))
PJ5 = Pin((__chip_num, 293))
PJ6 = Pin((__chip_num, 294))
PJ7 = Pin((__chip_num, 295))
PJ8 = Pin((__chip_num, 296))
PJ9 = Pin((__chip_num, 297))
PJ10 = Pin((__chip_num, 298))
PJ11 = Pin((__chip_num, 299))
PJ12 = Pin((__chip_num, 300))
PJ13 = Pin((__chip_num, 301))
PJ14 = Pin((__chip_num, 302))
PJ15 = Pin((__chip_num, 303))
PJ16 = Pin((__chip_num, 304))
PJ17 = Pin((__chip_num, 305))
PJ18 = Pin((__chip_num, 306))
PJ19 = Pin((__chip_num, 307))
PJ20 = Pin((__chip_num, 308))
PJ21 = Pin((__chip_num, 309))
PJ22 = Pin((__chip_num, 310))
PJ23 = Pin((__chip_num, 311))
PJ24 = Pin((__chip_num, 312))
PJ25 = Pin((__chip_num, 313))
PJ26 = Pin((__chip_num, 314))
PJ27 = Pin((__chip_num, 315))

PK0 = Pin((__chip_num, 320))
PK1 = Pin((__chip_num, 321))
PK2 = Pin((__chip_num, 322))
PK3 = Pin((__chip_num, 323))
PK4 = Pin((__chip_num, 324))
PK5 = Pin((__chip_num, 325))
PK6 = Pin((__chip_num, 326))
PK7 = Pin((__chip_num, 327))
PK8 = Pin((__chip_num, 328))
PK9 = Pin((__chip_num, 329))
PK10 = Pin((__chip_num, 330))
PK11 = Pin((__chip_num, 331))
PK12 = Pin((__chip_num, 332))
PK13 = Pin((__chip_num, 333))
PK14 = Pin((__chip_num, 334))
PK15 = Pin((__chip_num, 335))
PK16 = Pin((__chip_num, 336))
PK17 = Pin((__chip_num, 337))
PK18 = Pin((__chip_num, 338))
PK19 = Pin((__chip_num, 339))
PK20 = Pin((__chip_num, 340))
PK21 = Pin((__chip_num, 341))
PK22 = Pin((__chip_num, 342))
PK23 = Pin((__chip_num, 343))

PL0 = Pin((__chip_r_num, 0))
PL1 = Pin((__chip_r_num, 1))
PL2 = Pin((__chip_r_num, 2))
PL3 = Pin((__chip_r_num, 3))
PL4 = Pin((__chip_r_num, 4))
PL5 = Pin((__chip_r_num, 5))
PL6 = Pin((__chip_r_num, 6))
PL7 = Pin((__chip_r_num, 7))
PL8 = Pin((__chip_r_num, 8))
PL9 = Pin((__chip_r_num, 9))
PL10 = Pin((__chip_r_num, 10))
PL11 = Pin((__chip_r_num, 11))
PL12 = Pin((__chip_r_num, 12))
PL13 = Pin((__chip_r_num, 13))

PM0 = Pin((__chip_r_num, 32))
PM1 = Pin((__chip_r_num, 33))
PM2 = Pin((__chip_r_num, 34))
PM3 = Pin((__chip_r_num, 35))
PM4 = Pin((__chip_r_num, 36))
PM5 = Pin((__chip_r_num, 37))

# I2C
I2C1_SCL = PB4
I2C1_SDA = PB5
I2C4_SCL = PI0
I2C4_SDA = PI1
I2C5_SCL = PI8
I2C5_SDA = PI9

i2cPorts = (
    (1, I2C1_SCL, I2C1_SDA),
    (4, I2C4_SCL, I2C4_SDA),
    (5, I2C5_SCL, I2C5_SDA),
)

# SPI
SPI1_MOSI = PI4
SPI1_MISO = PI5
SPI1_SCLK = PI3
SPI1_CS0 = PI2
SPI2_MOSI = PB2
SPI2_MISO = PB3
SPI2_SCLK = PB1
SPI2_CS0 = PB0

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),
    (2, SPI2_SCLK, SPI2_MOSI, SPI2_MISO),
)

# UART
UART2_TX = PB0
UART2_RX = PB1
UART3_TX = PI11
UART3_RX = PI12
UART4_TX = PI0
UART4_RX = PI1
UART5_TX = PI2
UART5_RX = PI3
UART6_TX = PI6
UART6_RX = PI7
UART7_TX = PB13
UART7_RX = PB14

# ordered as uartId, txId, rxId
uartPorts = (
    (2, UART2_TX, UART2_RX),
    (3, UART3_TX, UART3_RX),
    (4, UART4_TX, UART4_RX),
    (5, UART5_TX, UART5_RX),
    (6, UART6_TX, UART6_RX),
    (7, UART7_TX, UART7_RX),
)

# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = [
    ((0, 1), PI0),
    ((0, 2), PI1),
    ((0, 3), PI2),
    ((0, 4), PI3),
    ((0, 5), PI4),
    ((0, 6), PI5),
    ((0, 7), PI6),
    ((0, 8), PI7),
    ((0, 9), PI8),
    ((0, 10), PI9),
    ((0, 11), PI10),
    ((0, 12), PI11),
    ((0, 13), PI12),
]
