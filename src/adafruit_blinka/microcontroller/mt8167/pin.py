# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""MediaTek MT8167 pin names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# All pins
GPIO52 = Pin(52)  # SDA1      (pin 3)
GPIO53 = Pin(53)  # SCL1      (pin 5)
GPIO22 = Pin(22)  # EINT22    (pin 7)
GPIO63 = Pin(63)  # UTXD0     (pin 8)
GPIO62 = Pin(62)  # URXD0     (pin 10)
GPIO9 = Pin(9)  # EINT9     (pin 11)
GPIO36 = Pin(36)  # MRG_CLK   (pin 12)
GPIO10 = Pin(10)  # EINT10    (pin 13)
GPIO11 = Pin(11)  # EINT11    (pin 15)
GPIO0 = Pin(0)  # EINT0     (pin 16)
GPIO1 = Pin(1)  # EINT1     (pin 18)
GPIO4 = Pin(4)  # EINT4     (pin 19)
GPIO3 = Pin(3)  # EINT3     (pin 21)
GPIO7 = Pin(7)  # EINT7     (pin 22)
GPIO6 = Pin(6)  # EINT6     (pin 23)
GPIO5 = Pin(5)  # EINT5     (pin 24)
GPIO8 = Pin(8)  # EINT8     (pin 26)
GPIO60 = Pin(60)  # SDA2      (pin 27)
GPIO61 = Pin(61)  # SCL2      (pin 28)
GPIO65 = Pin(65)  # UTXD1     (pin 29)
GPIO64 = Pin(64)  # URXD1     (pin 31)
GPIO12 = Pin(12)  # EINT12    (pin 32)
GPIO25 = Pin(25)  # EINT25    (pin 33)
GPIO37 = Pin(37)  # MRG_SYNC  (pin 35)
GPIO13 = Pin(13)  # EINT13    (pin 36)
GPIO45 = Pin(45)  # JTCLK     (pin 37)
GPIO38 = Pin(38)  # MRG_DI    (pin 38)
GPIO39 = Pin(39)  # MRG_DO    (pin 40)

# Aliases
PWM_A = GPIO25  # EINT12  (pin 32)
PWM_B = GPIO11  # EINT25  (pin 33)
PWM_C = GPIO12  # EINT11  (pin 15)

I2C1_SDA = GPIO52  # SDA1  (pin 3)
I2C1_SCL = GPIO53  # SCL1  (pin 5)

I2C2_SDA = GPIO60  # SDA2  (pin 27)
I2C2_SCL = GPIO61  # SCL2  (pin 28)

SPI_MO = GPIO4  # EINT4  (pin 19)
SPI_MI = GPIO3  # EINT3  (pin 21)
SPI_CLK = GPIO6  # EINT6  (pin 23)
SPI_CSB = GPIO5  # EINT5  (pin 24)

# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = (
    ((0, 0), PWM_A),
    ((0, 1), PWM_B),
    ((0, 2), PWM_C),
)

# ordered as i2cId, sclId, sdaId
i2cPorts = (
    (3, I2C1_SCL, I2C1_SDA),
    (0, I2C2_SCL, I2C2_SDA),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI_CLK, SPI_MO, SPI_MI),)
