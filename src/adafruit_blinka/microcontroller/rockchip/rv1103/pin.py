# SPDX-FileCopyrightText: 2022 ShangYun
#
# SPDX-License-Identifier: MIT
"""A Pin class for use with Rockchip RV1103."""
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

# UART
UART0_TX_M1 = GPIO2_B1
UART0_RX_M1 = GPIO2_B0
UART0_CTS_M1 = GPIO2_A7
UART0_RTS_M1 = GPIO2_A6
UART1_TX_M1 = GPIO2_A4
UART1_RX_M1 = GPIO2_A5
UART2_TX_M1 = GPIO1_B2
UART2_RX_M1 = GPIO1_B3
UART3_TX_M1 = GPIO1_D0
UART3_RX_M1 = GPIO1_D1
UART4_TX_M1 = GPIO1_C5
UART4_RX_M1 = GPIO1_C4
UART4_CTS_M1 = GPIO1_C7
UART4_RTS_M1 = GPIO1_C6
UART5_TX_M0 = GPIO3_A6
UART5_RX_M0 = GPIO3_A7

# ordered as uartId, txId, rxId
uartPorts = (
    (0, UART0_TX_M1, UART0_RX_M1),
    (1, UART1_TX_M1, UART2_RX_M1),
    (2, UART2_TX_M1, UART2_RX_M1),
    (3, UART3_TX_M1, UART3_RX_M1),
    (4, UART4_TX_M1, UART4_RX_M1),
    (5, UART5_TX_M0, UART5_RX_M0),
)


# I2C
I2C0_SCL_M2 = GPIO3_A4
I2C0_SDA_M2 = GPIO3_A5
I2C1_SCL_M1 = GPIO2_B0
I2C1_SDA_M1 = GPIO2_B1
I2C3_SCL_M0 = GPIO2_A6
I2C3_SDA_M0 = GPIO2_A7
I2C3_SCL_M1 = GPIO1_D3
I2C3_SDA_M1 = GPIO1_D2
I2C4_SCL_M0 = GPIO2_A1
I2C4_SDA_M0 = GPIO2_A0

# ordered as i2cId, sclId, sdaId
i2cPorts = (
    (0, I2C0_SCL_M2, I2C0_SDA_M2),
    (1, I2C1_SCL_M1, I2C1_SDA_M1),
    (3, I2C3_SCL_M0, I2C3_SDA_M0),
    (3, I2C3_SCL_M1, I2C3_SDA_M1),
    (4, I2C4_SCL_M0, I2C4_SDA_M0),
)

# SPI
SPI0_MISO_M0 = GPIO1_C3
SPI0_MOSI_M0 = GPIO1_C2
SPI0_CLK_M0 = GPIO1_C1
SPI0_CS0_M0 = GPIO1_C0
SPI0_CS1_M0 = GPIO1_D2

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI0_CLK_M0, SPI0_MOSI_M0, SPI0_MISO_M0),)

# PWM
PWM0 = GPIO1_A2
PWM1 = GPIO0_A4
PWM5 = GPIO2_B0
PWM6 = GPIO2_B1
PWM10 = GPIO1_C6
PWM11 = GPIO1_C7

# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = (
    ((0, 0), PWM0),
    ((1, 0), PWM1),
    ((5, 0), PWM5),
    ((6, 0), PWM6),
    ((10, 0), PWM10),
    ((11, 0), PWM11),
)

# ADC IN
ADC_IN0 = 0
ADC_IN1 = 1

# SysFS analog inputs, Ordered as analog analogInId, device, and channel
analogIns = (
    (ADC_IN0, 0, 0),
    (ADC_IN1, 0, 1),
)
