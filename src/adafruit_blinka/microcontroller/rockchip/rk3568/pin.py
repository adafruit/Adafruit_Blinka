# SPDX-FileCopyrightText: 2023 mmontol
#
# SPDX-License-Identifier: MIT

"""A Pin class for use with Rockchip RK3568."""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# GPIO0
GPIO0_B0 = Pin((0, 8))
GPIO0_C2 = Pin((0, 18))

# GPIO1
GPIO1_A0 = Pin((1, 0))
GPIO1_A1 = Pin((1, 1))
GPIO1_B0 = Pin((1, 8))
GPIO1_B1 = Pin((1, 9))
GPIO1_B2 = Pin((1, 10))

# GPIO2
GPIO2_D7 = Pin((2, 31))

# GPIO3
GPIO3_A0 = Pin((3, 0))
GPIO3_A5 = Pin((3, 5))
GPIO3_A6 = Pin((3, 6))
GPIO3_A7 = Pin((3, 7))
GPIO3_B1 = Pin((3, 9))
GPIO3_B2 = Pin((3, 10))
GPIO3_B3 = Pin((3, 11))
GPIO3_B4 = Pin((3, 12))
GPIO3_B5 = Pin((3, 13))
GPIO3_B6 = Pin((3, 14))
GPIO3_B7 = Pin((3, 15))
GPIO3_C0 = Pin((3, 16))
GPIO3_C4 = Pin((3, 20))
GPIO3_C5 = Pin((3, 21))

# GPIO4
GPIO4_C2 = Pin((4, 18))
GPIO4_C3 = Pin((4, 19))
GPIO4_C4 = Pin((4, 20))
GPIO4_C5 = Pin((4, 21))
GPIO4_C6 = Pin((4, 22))
GPIO4_D2 = Pin((4, 26))

# I2C
I2C3_SCL_M0 = GPIO1_A1
I2C3_SDA_M0 = GPIO1_A0
I2C5_SCL_M0 = GPIO3_B3
I2C5_SDA_M0 = GPIO3_B4

# SPI
SPI3_CS0_M1 = GPIO4_C6
SPI3_CLK_M1 = GPIO4_C2
SPI3_MISO_M1 = GPIO4_C5
SPI3_MOSI_M1 = GPIO4_C3

# UART
UART3_TX_M1 = GPIO3_B7
UART3_RX_M1 = GPIO3_C0

# PWM
PWM8_M0 = GPIO3_B1
PWM9_M0 = GPIO3_B2
PWM10_M0 = GPIO3_B5
PWM14_M0 = GPIO3_C4

# ordered as i2cId, SCL, SDA
i2cPorts = (
    (3, I2C3_SCL_M0, I2C3_SDA_M0),
    (5, I2C5_SCL_M0, I2C5_SDA_M0),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((3, SPI3_CLK_M1, SPI3_MOSI_M1, SPI3_MISO_M1),)

# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = (
    ((1, 0), PWM8_M0),
    ((1, 0), PWM9_M0),
    ((1, 0), PWM10_M0),
    ((1, 0), PWM14_M0),
)

# SysFS analog inputs, Ordered as analog analogInId, device, and channel
