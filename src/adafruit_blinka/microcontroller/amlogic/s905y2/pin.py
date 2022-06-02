# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""AmLogic s905y2 pin names"""
# pylint: disable=wildcard-import,unused-wildcard-import
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

periphs = 0
aobus = 1

GPIO412 = GPIOAO_0 = Pin((aobus, 0))
GPIO413 = GPIOAO_1 = Pin((aobus, 1))
GPIO414 = GPIOAO_2 = Pin((aobus, 2))
GPIO415 = GPIOAO_3 = Pin((aobus, 3))
GPIO416 = GPIOAO_4 = Pin((aobus, 4))

GPIO420 = GPIOAO_8 = Pin((aobus, 8))
GPIO421 = GPIOAO_9 = Pin((aobus, 9))
GPIO422 = GPIOAO_10 = Pin((aobus, 10))
GPIO423 = GPIOAO_11 = Pin((aobus, 11))

GPIO447 = GPIOH_4 = Pin((periphs, 20))
GPIO448 = GPIOH_5 = Pin((periphs, 21))
GPIO449 = GPIOH_6 = Pin((periphs, 22))
GPIO450 = GPIOH_7 = Pin((periphs, 23))
GPIO451 = GPIOH_8 = Pin((periphs, 24))

GPIO490 = GPIOA_14 = Pin((periphs, 63))
GPIO491 = GPIOA_15 = Pin((periphs, 64))


GPIO500 = GPIOX_8 = Pin((periphs, 73))
GPIO501 = GPIOX_9 = Pin((periphs, 74))
GPIO502 = GPIOX_10 = Pin((periphs, 75))
GPIO503 = GPIOX_11 = Pin((periphs, 76))


I2C1_SDA = GPIOH_6
I2C1_SCL = GPIOH_7
I2C3_SDA = GPIOA_14
I2C3_SCL = GPIOA_15
I2C4_SDA = GPIOAO_3
I2C4_SCL = GPIOAO_2

SPIA_SCLK = GPIOX_11
SPIA_MISO = GPIOX_9
SPIA_MOSI = GPIOX_8

SPIB_SCLK = GPIOH_7
SPIB_MISO = GPIOH_5
SPIB_MOSI = GPIOH_4

UARTA_TX = GPIOAO_2
UARTA_RX = GPIOAO_3
UARTB_TX = GPIOAO_8
UARTB_RX = GPIOAO_9
UARTC_TX = GPIOH_7
UARTC_RX = GPIOH_6

i2cPorts = (
    (1, I2C1_SCL, I2C1_SDA),
    (3, I2C3_SCL, I2C3_SDA),
    (4, I2C4_SCL, I2C4_SDA),
)

spiPorts = (
    (0, SPIA_SCLK, SPIA_MOSI, SPIA_MISO),
    (1, SPIB_SCLK, SPIB_MOSI, SPIB_MISO),
)

uartPorts = (
    (0, UARTA_TX, UARTA_RX),
    (1, UARTB_TX, UARTB_RX),
    (4, UARTC_TX, UARTC_RX),
)
