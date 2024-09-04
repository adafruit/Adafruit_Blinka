# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Spacemit K1 Pin Names"""
from adafruit_blinka.agnostic import detector
from adafruit_blinka.microcontroller.alias import get_pwm_chipid
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

__chip_num = 0

GPIO_0 = Pin((__chip_num, 0))
GPIO_1 = Pin((__chip_num, 1))
GPIO_2 = Pin((__chip_num, 2))
GPIO_3 = Pin((__chip_num, 3))
GPIO_4 = Pin((__chip_num, 4))
GPIO_5 = Pin((__chip_num, 5))
GPIO_6 = Pin((__chip_num, 6))
GPIO_7 = Pin((__chip_num, 7))
GPIO_8 = Pin((__chip_num, 8))
GPIO_9 = Pin((__chip_num, 9))
GPIO_10 = Pin((__chip_num, 10))
GPIO_11 = Pin((__chip_num, 11))
GPIO_12 = Pin((__chip_num, 12))
GPIO_13 = Pin((__chip_num, 13))
GPIO_14 = Pin((__chip_num, 14))
GPIO_15 = Pin((__chip_num, 15))
GPIO_16 = Pin((__chip_num, 16))
GPIO_17 = Pin((__chip_num, 17))
GPIO_18 = Pin((__chip_num, 18))
GPIO_19 = Pin((__chip_num, 19))
GPIO_20 = Pin((__chip_num, 20))
GPIO_21 = Pin((__chip_num, 21))
GPIO_22 = Pin((__chip_num, 22))
GPIO_23 = Pin((__chip_num, 23))
GPIO_24 = Pin((__chip_num, 24))
GPIO_25 = Pin((__chip_num, 25))
GPIO_26 = Pin((__chip_num, 26))
GPIO_27 = Pin((__chip_num, 27))
GPIO_28 = Pin((__chip_num, 28))
GPIO_29 = Pin((__chip_num, 29))
GPIO_30 = Pin((__chip_num, 30))
GPIO_31 = Pin((__chip_num, 31))
GPIO_32 = Pin((__chip_num, 32))
GPIO_33 = Pin((__chip_num, 33))
GPIO_34 = Pin((__chip_num, 34))
GPIO_35 = Pin((__chip_num, 35))
GPIO_36 = Pin((__chip_num, 36))
GPIO_37 = Pin((__chip_num, 37))
GPIO_38 = Pin((__chip_num, 38))
GPIO_39 = Pin((__chip_num, 39))
GPIO_40 = Pin((__chip_num, 40))
GPIO_41 = Pin((__chip_num, 41))
GPIO_42 = Pin((__chip_num, 42))
GPIO_43 = Pin((__chip_num, 43))
GPIO_44 = Pin((__chip_num, 44))
GPIO_45 = Pin((__chip_num, 45))
GPIO_46 = Pin((__chip_num, 46))
GPIO_47 = Pin((__chip_num, 47))
GPIO_48 = Pin((__chip_num, 48))
GPIO_49 = Pin((__chip_num, 49))
GPIO_50 = Pin((__chip_num, 50))
GPIO_51 = Pin((__chip_num, 51))
GPIO_52 = Pin((__chip_num, 52))
GPIO_53 = Pin((__chip_num, 53))
GPIO_54 = Pin((__chip_num, 54))
GPIO_55 = Pin((__chip_num, 55))
GPIO_56 = Pin((__chip_num, 56))
GPIO_57 = Pin((__chip_num, 57))
GPIO_58 = Pin((__chip_num, 58))
GPIO_59 = Pin((__chip_num, 59))
GPIO_60 = Pin((__chip_num, 60))
GPIO_61 = Pin((__chip_num, 61))
GPIO_62 = Pin((__chip_num, 62))
GPIO_63 = Pin((__chip_num, 63))
GPIO_64 = Pin((__chip_num, 64))
GPIO_65 = Pin((__chip_num, 65))
GPIO_66 = Pin((__chip_num, 66))
GPIO_67 = Pin((__chip_num, 67))
GPIO_68 = Pin((__chip_num, 68))
GPIO_69 = Pin((__chip_num, 69))
GPIO_70 = Pin((__chip_num, 70))
GPIO_71 = Pin((__chip_num, 71))
GPIO_72 = Pin((__chip_num, 72))
GPIO_73 = Pin((__chip_num, 73))
GPIO_74 = Pin((__chip_num, 74))
GPIO_75 = Pin((__chip_num, 75))
GPIO_76 = Pin((__chip_num, 76))
GPIO_77 = Pin((__chip_num, 77))
GPIO_78 = Pin((__chip_num, 78))
GPIO_79 = Pin((__chip_num, 79))
GPIO_80 = Pin((__chip_num, 80))
GPIO_81 = Pin((__chip_num, 81))
GPIO_82 = Pin((__chip_num, 82))
GPIO_83 = Pin((__chip_num, 83))
GPIO_84 = Pin((__chip_num, 84))
GPIO_85 = Pin((__chip_num, 85))
GPIO_86 = Pin((__chip_num, 86))
GPIO_87 = Pin((__chip_num, 87))
GPIO_88 = Pin((__chip_num, 88))
GPIO_89 = Pin((__chip_num, 89))
GPIO_90 = Pin((__chip_num, 90))
GPIO_91 = Pin((__chip_num, 91))
GPIO_92 = Pin((__chip_num, 92))
GPIO_93 = Pin((__chip_num, 93))
GPIO_94 = Pin((__chip_num, 94))
GPIO_95 = Pin((__chip_num, 95))
GPIO_96 = Pin((__chip_num, 96))
GPIO_97 = Pin((__chip_num, 97))
GPIO_98 = Pin((__chip_num, 98))
GPIO_99 = Pin((__chip_num, 99))
GPIO_100 = Pin((__chip_num, 100))
GPIO_101 = Pin((__chip_num, 101))
GPIO_102 = Pin((__chip_num, 102))
GPIO_103 = Pin((__chip_num, 103))
GPIO_104 = Pin((__chip_num, 104))
GPIO_105 = Pin((__chip_num, 105))
GPIO_106 = Pin((__chip_num, 106))
GPIO_107 = Pin((__chip_num, 107))
GPIO_108 = Pin((__chip_num, 108))
GPIO_109 = Pin((__chip_num, 109))
GPIO_110 = Pin((__chip_num, 110))
GPIO_111 = Pin((__chip_num, 111))
GPIO_112 = Pin((__chip_num, 112))
GPIO_113 = Pin((__chip_num, 113))
GPIO_114 = Pin((__chip_num, 114))
GPIO_115 = Pin((__chip_num, 115))
GPIO_116 = Pin((__chip_num, 116))
GPIO_117 = Pin((__chip_num, 117))
GPIO_118 = Pin((__chip_num, 118))
GPIO_119 = Pin((__chip_num, 119))
GPIO_120 = Pin((__chip_num, 120))
GPIO_121 = Pin((__chip_num, 121))
GPIO_122 = Pin((__chip_num, 122))
GPIO_123 = Pin((__chip_num, 123))
GPIO_124 = Pin((__chip_num, 124))
GPIO_125 = Pin((__chip_num, 125))
GPIO_126 = Pin((__chip_num, 126))
GPIO_127 = Pin((__chip_num, 127))

# I2C
I2C4_SCL = GPIO_51
I2C4_SDA = GPIO_52

i2cPorts = ((4, I2C4_SCL, I2C4_SDA),)

# SPI
SPI3_MISO = GPIO_78
SPI3_MOSI = GPIO_77
SPI3_SCLK = GPIO_75
SPI3_CS0 = GPIO_76

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((3, SPI3_SCLK, SPI3_MOSI, SPI3_MISO),)

# UART
UART0_TX = GPIO_47
UART0_RX = GPIO_48

# ordered as uartId, txId, rxId
uartPorts = ((0, UART0_TX, UART0_RX),)

# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = []

board = detector.board.id
if board in ("BANANA_PI_F3"):
    alias = get_pwm_chipid("d401bc00.pwm")
    if alias is not None:
        globals()["PWM" + alias] = GPIO_92
        pwmOuts.append(((int(alias[-1]), 0), GPIO_92))
    alias = get_pwm_chipid("d4020400.pwm")
    if alias is not None:
        globals()["PWM" + alias] = GPIO_74
        pwmOuts.append(((int(alias[-1]), 0), GPIO_74))
