# SPDX-FileCopyrightText: 2022 Kenneth Ryerson
#
# SPDX-License-Identifier: MIT

"""A Pin class for use with Rockchip RK3566."""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

GPIO0_A2 = Pin((0, 2))
GPIO0_A4 = Pin((0, 4))
GPIO0_A5 = Pin((0, 5))
GPIO0_B1 = Pin((0, 9))
GPIO0_B2 = Pin((0, 10))
GPIO0_B5 = Pin((0, 13))
GPIO0_B6 = Pin((0, 14))
GPIO0_B7 = Pin((0, 15))
GPIO0_C2 = Pin((0, 18))
GPIO0_C3 = Pin((0, 19))
GPIO0_C5 = Pin((0, 21))
GPIO0_C6 = Pin((0, 22))
GPIO0_C7 = Pin((0, 23))
GPIO0_D0 = Pin((0, 24))
GPIO0_D1 = Pin((0, 25))
GPIO1_A0 = Pin((1, 0))
GPIO1_A1 = Pin((1, 1))
GPIO1_A2 = Pin((1, 2))
GPIO1_A3 = Pin((1, 3))
GPIO1_A4 = Pin((1, 4))
GPIO1_A5 = Pin((1, 5))
GPIO1_A7 = Pin((1, 7))
GPIO1_B0 = Pin((1, 8))
GPIO1_B1 = Pin((1, 9))
GPIO1_B2 = Pin((1, 10))
GPIO1_B3 = Pin((1, 11))
GPIO1_D5 = Pin((1, 29))
GPIO1_D6 = Pin((1, 30))
GPIO1_D7 = Pin((1, 31))
GPIO2_A0 = Pin((2, 0))
GPIO2_A1 = Pin((2, 1))
GPIO2_A2 = Pin((2, 2))
GPIO2_C3 = Pin((2, 19))
GPIO2_C4 = Pin((2, 20))
GPIO2_C5 = Pin((2, 21))
GPIO2_C6 = Pin((2, 22))
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

ADC_AIN3 = 37

# I2C
I2C0_SCL = GPIO0_B1
I2C0_SDA = GPIO0_B2
I2C2_SCL_M0 = GPIO0_B5
I2C2_SDA_M0 = GPIO0_B6
I2C2_SCL_M1 = GPIO4_B5
I2C2_SDA_M1 = GPIO4_B4
I2C3_SCL_M0 = GPIO1_A1
I2C3_SDA_M0 = GPIO1_A0
I2C4_SCL_M0 = GPIO4_B3
I2C4_SDA_M0 = GPIO4_B2
I2C5_SCL_M0 = GPIO3_B3
I2C5_SDA_M0 = GPIO3_B4

# SPI
SPI0_CS0_M0 = GPIO0_C6
SPI0_CLK_M0 = GPIO0_B5
SPI0_MISO_M0 = GPIO0_C5
SPI0_MOSI_M0 = GPIO0_B6
SPI3_CS0_M0 = GPIO4_A6
SPI3_CLK_M0 = GPIO4_B3
SPI3_MISO_M0 = GPIO4_B0
SPI3_MOSI_M0 = GPIO4_B2
SPI3_CS0_M1 = GPIO4_C6
SPI3_CLK_M1 = GPIO4_C2
SPI3_MISO_M1 = GPIO4_C5
SPI3_MOSI_M1 = GPIO4_C3

# UART
UART2_TX = GPIO0_D1
UART2_RX = GPIO0_D0
UART3_TX_M1 = GPIO3_B7
UART3_RX_M1 = GPIO3_C0
UART8_TX_M0 = GPIO2_C5
UART8_RX_M0 = GPIO2_C6

# PWM
PWM0 = GPIO0_B7
PWM1 = GPIO0_C7

# ordered as i2cId, SCL, SDA
i2cPorts = (
    (2, I2C2_SCL_M0, I2C2_SDA_M0),
    (3, I2C3_SCL_M0, I2C3_SDA_M0),
    (5, I2C5_SCL_M0, I2C5_SDA_M0),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (3, SPI3_CLK_M0, SPI3_MOSI_M0, SPI3_MISO_M0),
    (3, SPI3_CLK_M1, SPI3_MOSI_M1, SPI3_MISO_M1),
)

# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = (
    ((0, 0), PWM0),
    ((0, 0), PWM1),
)

# SysFS analog inputs, Ordered as analog analogInId, device, and channel
analogIns = ((ADC_AIN3, 0, 3),)
