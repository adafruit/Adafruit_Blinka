# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
# See https://wiki.radxa.com/Rock4/hardware/gpio
#
# SPDX-License-Identifier: MIT
"""A Pin class for use with Rockchip RK3399 and RK3399_T."""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# GPIOx_yz = x * 32 + y * 8 + z
# y: A -> 0, B -> 1, C -> 2, D -> 3

GPIO0_A0 = Pin((0, 0))
GPIO0_A1 = Pin((0, 1))
GPIO0_A2 = Pin((0, 2))
GPIO0_A3 = Pin((0, 3))
GPIO0_A4 = Pin((0, 4))
GPIO0_A5 = Pin((0, 5))
GPIO0_A6 = Pin((0, 6))
GPIO0_A7 = Pin((0, 7))
GPIO0_B0 = Pin((0, 8))
GPIO0_B1 = Pin((0, 9))
GPIO0_B2 = Pin((0, 10))
GPIO0_B3 = Pin((0, 11))
GPIO0_B4 = Pin((0, 12))
GPIO0_B5 = Pin((0, 13))
GPIO0_B6 = Pin((0, 14))
GPIO0_B7 = Pin((0, 15))
GPIO0_C0 = Pin((0, 16))
GPIO0_C1 = Pin((0, 17))
GPIO0_C2 = Pin((0, 18))
GPIO0_C3 = Pin((0, 19))
GPIO0_C4 = Pin((0, 20))
GPIO0_C5 = Pin((0, 21))
GPIO0_C6 = Pin((0, 22))
GPIO0_C7 = Pin((0, 23))
GPIO0_D0 = Pin((0, 24))
GPIO0_D1 = Pin((0, 25))
GPIO0_D2 = Pin((0, 26))
GPIO0_D3 = Pin((0, 27))
GPIO0_D4 = Pin((0, 28))
GPIO0_D5 = Pin((0, 29))
GPIO0_D6 = Pin((0, 30))
GPIO0_D7 = Pin((0, 31))

GPIO1_A0 = Pin((1, 0))
GPIO1_A1 = Pin((1, 1))
GPIO1_A2 = Pin((1, 2))
GPIO1_A3 = Pin((1, 3))
GPIO1_A4 = Pin((1, 4))
GPIO1_A5 = Pin((1, 5))
GPIO1_A6 = Pin((1, 6))
GPIO1_A7 = Pin((1, 7))
GPIO1_B0 = Pin((1, 8))
GPIO1_B1 = Pin((1, 9))
GPIO1_B2 = Pin((1, 10))
GPIO1_B3 = Pin((1, 11))
GPIO1_B4 = Pin((1, 12))
GPIO1_B5 = Pin((1, 13))
GPIO1_B6 = Pin((1, 14))
GPIO1_B7 = Pin((1, 15))
GPIO1_C0 = Pin((1, 16))
GPIO1_C1 = Pin((1, 17))
GPIO1_C2 = Pin((1, 18))
GPIO1_C3 = Pin((1, 19))
GPIO1_C4 = Pin((1, 20))
GPIO1_C5 = Pin((1, 21))
GPIO1_C6 = Pin((1, 22))
GPIO1_C7 = Pin((1, 23))
GPIO1_D0 = Pin((1, 24))
GPIO1_D1 = Pin((1, 25))
GPIO1_D2 = Pin((1, 26))
GPIO1_D3 = Pin((1, 27))
GPIO1_D4 = Pin((1, 28))
GPIO1_D5 = Pin((1, 29))
GPIO1_D6 = Pin((1, 30))
GPIO1_D7 = Pin((1, 31))

GPIO2_A0 = Pin((2, 0))
GPIO2_A1 = Pin((2, 1))
GPIO2_A2 = Pin((2, 2))
GPIO2_A3 = Pin((2, 3))
GPIO2_A4 = Pin((2, 4))
GPIO2_A5 = Pin((2, 5))
GPIO2_A6 = Pin((2, 6))
GPIO2_A7 = Pin((2, 7))
GPIO2_B0 = Pin((2, 8))
GPIO2_B1 = Pin((2, 9))
GPIO2_B2 = Pin((2, 10))
GPIO2_B3 = Pin((2, 11))
GPIO2_B4 = Pin((2, 12))
GPIO2_B5 = Pin((2, 13))
GPIO2_B6 = Pin((2, 14))
GPIO2_B7 = Pin((2, 15))
GPIO2_C0 = Pin((2, 16))
GPIO2_C1 = Pin((2, 17))
GPIO2_C2 = Pin((2, 18))
GPIO2_C3 = Pin((2, 19))
GPIO2_C4 = Pin((2, 20))
GPIO2_C5 = Pin((2, 21))
GPIO2_C6 = Pin((2, 22))
GPIO2_C7 = Pin((2, 23))
GPIO2_D0 = Pin((2, 24))
GPIO2_D1 = Pin((2, 25))
GPIO2_D2 = Pin((2, 26))
GPIO2_D3 = Pin((2, 27))
GPIO2_D4 = Pin((2, 28))
GPIO2_D5 = Pin((2, 29))
GPIO2_D6 = Pin((2, 30))
GPIO2_D7 = Pin((2, 31))

GPIO3_A0 = Pin((3, 0))
GPIO3_A1 = Pin((3, 1))
GPIO3_A2 = Pin((3, 2))
GPIO3_A3 = Pin((3, 3))
GPIO3_A4 = Pin((3, 4))
GPIO3_A5 = Pin((3, 5))
GPIO3_A6 = Pin((3, 6))
GPIO3_A7 = Pin((3, 7))
GPIO3_B0 = Pin((3, 8))
GPIO3_B1 = Pin((3, 9))
GPIO3_B2 = Pin((3, 10))
GPIO3_B3 = Pin((3, 11))
GPIO3_B4 = Pin((3, 12))
GPIO3_B5 = Pin((3, 13))
GPIO3_B6 = Pin((3, 14))
GPIO3_B7 = Pin((3, 15))
GPIO3_C0 = Pin((3, 16))
GPIO3_C1 = Pin((3, 17))
GPIO3_C2 = Pin((3, 18))
GPIO3_C3 = Pin((3, 19))
GPIO3_C4 = Pin((3, 20))
GPIO3_C5 = Pin((3, 21))
GPIO3_C6 = Pin((3, 22))
GPIO3_C7 = Pin((3, 23))
GPIO3_D0 = Pin((3, 24))
GPIO3_D1 = Pin((3, 25))
GPIO3_D2 = Pin((3, 26))
GPIO3_D3 = Pin((3, 27))
GPIO3_D4 = Pin((3, 28))
GPIO3_D5 = Pin((3, 29))
GPIO3_D6 = Pin((3, 30))
GPIO3_D7 = Pin((3, 31))

GPIO4_A0 = Pin((4, 0))
GPIO4_A1 = Pin((4, 1))
GPIO4_A2 = Pin((4, 2))
GPIO4_A3 = Pin((4, 3))
GPIO4_A4 = Pin((4, 4))
GPIO4_A5 = Pin((4, 5))
GPIO4_A6 = Pin((4, 6))
GPIO4_A7 = Pin((4, 7))
GPIO4_B0 = Pin((4, 8))
GPIO4_B1 = Pin((4, 9))
GPIO4_B2 = Pin((4, 10))
GPIO4_B3 = Pin((4, 11))
GPIO4_B4 = Pin((4, 12))
GPIO4_B5 = Pin((4, 13))
GPIO4_B6 = Pin((4, 14))
GPIO4_B7 = Pin((4, 15))
GPIO4_C0 = Pin((4, 16))
GPIO4_C1 = Pin((4, 17))
GPIO4_C2 = Pin((4, 18))
GPIO4_C3 = Pin((4, 19))
GPIO4_C4 = Pin((4, 20))
GPIO4_C5 = Pin((4, 21))
GPIO4_C6 = Pin((4, 22))
GPIO4_C7 = Pin((4, 23))
GPIO4_D0 = Pin((4, 24))
GPIO4_D1 = Pin((4, 25))
GPIO4_D2 = Pin((4, 26))
GPIO4_D3 = Pin((4, 27))
GPIO4_D4 = Pin((4, 28))
GPIO4_D5 = Pin((4, 29))
GPIO4_D6 = Pin((4, 30))
GPIO4_D7 = Pin((4, 31))

ADC_IN0 = 1
ADC_IN1 = 2
ADC_IN2 = 3
ADC_IN3 = 4
ADC_IN4 = 5
ADC_IN5 = 6

# I2C
I2C2_SDA = GPIO2_A0
I2C2_SCL = GPIO2_A1
I2C3_SDA = GPIO4_C0
I2C3_SCL = GPIO4_C1
I2C6_SDA = GPIO2_B1
I2C6_SCL = GPIO2_B2
I2C7_SDA = GPIO2_A7
I2C7_SCL = GPIO2_B0
I2C8_SDA = GPIO1_C4
I2C8_SCL = GPIO1_C5

# SPI
SPI1_CS = GPIO1_B2
SPI1_SCLK = GPIO1_B1
SPI1_MISO = GPIO1_A7
SPI1_MOSI = GPIO1_B0
SPI2_CS = GPIO2_B4
SPI2_SCLK = GPIO2_B3
SPI2_MISO = GPIO2_B1
SPI2_MOSI = GPIO2_B2

# UART
UART2_TX = GPIO4_C4
UART2_RX = GPIO4_C3
UART4_TX = GPIO1_B0
UART4_RX = GPIO1_A7

# PWM
PWM0 = GPIO4_C2
PWM1 = GPIO4_C6
PWM2 = GPIO1_C3

# ordered as i2cId, SCL, SDA
i2cPorts = (
    (2, I2C2_SCL, I2C2_SDA),
    (6, I2C6_SCL, I2C6_SDA),
    (7, I2C7_SCL, I2C7_SDA),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),
    (2, SPI2_SCLK, SPI2_MOSI, SPI2_MISO),
)

# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = (
    ((0, 0), PWM0),
    ((1, 0), PWM1),
    ((2, 0), PWM2),
)

# SysFS analog inputs, Ordered as analog analogInId, device, and channel
analogIns = (
    (ADC_IN0, 0, 0),
    (ADC_IN1, 0, 1),
    (ADC_IN2, 0, 2),
    (ADC_IN3, 0, 3),
    (ADC_IN4, 0, 4),
    (ADC_IN5, 0, 5),
)
