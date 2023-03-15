# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
# See https://wiki.radxa.com/Rock4/hardware/gpio
#
# SPDX-License-Identifier: MIT
"""A Pin class for use with Rockchip RK3399 and RK3399_T."""

from adafruit_blinka.microcontroller.generic_linux.sysfs_pin import Pin

GPIO1_A1 = Pin(33)
GPIO1_A3 = Pin(35)
GPIO1_A7 = Pin(39)
GPIO1_B0 = Pin(40)
GPIO1_B1 = Pin(41)
GPIO1_B2 = Pin(42)
GPIO1_C2 = Pin(50)
GPIO1_C4 = Pin(52)
GPIO1_C5 = Pin(53)
GPIO1_C6 = Pin(54)
GPIO1_C7 = Pin(55)
GPIO1_D0 = Pin(56)
GPIO2_A0 = Pin(64)
GPIO2_A1 = Pin(65)
GPIO2_A7 = Pin(71)
GPIO2_B0 = Pin(72)
GPIO2_B1 = Pin(73)
GPIO2_B2 = Pin(74)
GPIO2_B3 = Pin(75)
GPIO2_B4 = Pin(76)
GPIO2_D4 = Pin(92)
GPIO3_C0 = Pin(112)
GPIO4_A3 = Pin(131)
GPIO4_A4 = Pin(132)
GPIO4_A5 = Pin(133)
GPIO4_A6 = Pin(134)
GPIO4_A7 = Pin(135)
GPIO4_C0 = Pin(144)
GPIO4_C1 = Pin(145)
GPIO4_C2 = Pin(146)
GPIO4_C3 = Pin(147)
GPIO4_C4 = Pin(148)
GPIO4_C5 = Pin(149)
GPIO4_C6 = Pin(150)
GPIO4_D2 = Pin(154)
GPIO4_D4 = Pin(156)
GPIO4_D5 = Pin(157)
GPIO4_D6 = Pin(158)
ADC_IN0 = 1

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
    ((0, 0), PWM1),
)

# SysFS analog inputs, Ordered as analog analogInId, device, and channel
analogIns = ((ADC_IN0, 0, 0),)
