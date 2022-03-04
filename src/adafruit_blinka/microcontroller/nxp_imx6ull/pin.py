# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""NXP IMX6ULL pin names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# GPIO num = reconment function = Pin((chip, line))
GPIO31 = I2C2_SDA = Pin((0, 31))  # GPIO1_IO31
GPIO30 = I2C2_SCL = Pin((0, 30))  # GPIO1_IO30

GPIO29 = I2C3_SDA = Pin((0, 29))  # GPIO1_IO29
GPIO28 = I2C3_SCL = Pin((0, 28))  # GPIO1_IO28

GPIO24 = UART3_TXD = Pin((0, 24))  # GPIO1_IO24
GPIO25 = UART3_RXD = Pin((0, 25))  # GPIO1_IO25

GPIO22 = ECSPI3_MOSI = Pin((0, 22))  # GPIO1_IO22
GPIO23 = ECSPI3_MISO = Pin((0, 23))  # GPIO1_IO23
GPIO21 = ECSPI3_SCLK = Pin((0, 21))  # GPIO1_IO21
GPIO20 = ECSPI3_SS0 = Pin((0, 20))  # GPIO1_IO20
GPIO18 = ECSPI3_SS1 = Pin((0, 18))  # GPIO1_IO18

GPIO0 = ADC_IN0 = Pin((0, 0))  # GPIO1_IO0
GPIO1 = ADC_IN1 = Pin((0, 1))  # GPIO1_IO2
GPIO2 = ADC_IN2 = Pin((0, 2))  # GPIO1_IO2
GPIO3 = ADC_IN3 = Pin((0, 3))  # GPIO1_IO3
GPIO4 = PWM_C3 = Pin((0, 4))  # GPIO1_IO4
GPIO26 = Pin((0, 26))  # GPIO1_IO26
GPIO27 = Pin((0, 27))  # GPIO1_IO27

GPIO113 = Pin((3, 17))  # GPIO4_IO17
GPIO114 = Pin((3, 18))  # GPIO4_IO18
GPIO115 = PWM_C7 = Pin((3, 19))  # GPIO4_IO19
GPIO116 = PWM_C8 = Pin((3, 20))  # GPIO4_IO20
GPIO117 = Pin((3, 21))  # GPIO4_IO21
GPIO118 = Pin((3, 22))  # GPIO4_IO22
GPIO119 = Pin((3, 23))  # GPIO4_IO23
GPIO120 = Pin((3, 24))  # GPIO4_IO24
GPIO121 = Pin((3, 25))  # GPIO4_IO25
GPIO112 = Pin((3, 26))  # GPIO4_IO26
GPIO123 = Pin((3, 27))  # GPIO4_IO27
GPIO124 = Pin((3, 28))  # GPIO4_IO28

GPIO129 = Pin((4, 1))  # GPIO5_IO1

i2cPorts = (
    (1, I2C2_SCL, I2C2_SDA),
    (2, I2C3_SCL, I2C3_SDA),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((2, ECSPI3_SCLK, ECSPI3_MOSI, ECSPI3_MISO),)

# UART3_TXD/RXD on /dev/ttymxc2
uartPorts = ((2, UART3_TXD, UART3_RXD),)

# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = (
    ((2, 0), PWM_C3),
    ((6, 0), PWM_C7),
    ((7, 0), PWM_C8),
)

# SysFS analog inputs, Ordered as analog analogInId, device, and channel
analogIns = (
    (ADC_IN0, 0, 0),
    (ADC_IN1, 0, 1),
    (ADC_IN2, 0, 2),
    (ADC_IN3, 0, 3),
)
