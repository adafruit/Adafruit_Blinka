# SPDX-FileCopyrightText: 2026 Bert Outtier
#
# SPDX-License-Identifier: MIT
"""Allwinner T113-S3 pin names"""
from adafruit_blinka.microcontroller.alias import get_pwm_chipid
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PB2 = Pin(34)
PB3 = Pin(35)
PB4 = Pin(36)
PB5 = Pin(37)
PB6 = Pin(38)
PB7 = Pin(39)
PC2 = Pin(66)
PC3 = Pin(67)
PC4 = Pin(68)
PC5 = Pin(69)
PC6 = Pin(70)
PC7 = Pin(71)
PD0 = Pin(96)
PD1 = Pin(97)
PD2 = Pin(98)
PD3 = Pin(99)
PD4 = Pin(100)
PD5 = Pin(101)
PD6 = Pin(102)
PD7 = Pin(103)
PD8 = Pin(104)
PD9 = Pin(105)
PD10 = Pin(106)
PD11 = Pin(107)
PD12 = Pin(108)
PD13 = Pin(109)
PD14 = Pin(110)
PD15 = Pin(111)
PD16 = Pin(112)
PD17 = Pin(113)
PD18 = Pin(114)
PD19 = Pin(115)
PD20 = Pin(116)
PD21 = Pin(117)
PD22 = Pin(118)
PE0 = Pin(128)
PE1 = Pin(129)
PE2 = Pin(130)
PE3 = Pin(131)
PE4 = Pin(132)
PE5 = Pin(133)
PE6 = Pin(134)
PE7 = Pin(135)
PE8 = Pin(136)
PE9 = Pin(137)
PE10 = Pin(138)
PE11 = Pin(139)
PE12 = Pin(140)
PE13 = Pin(141)
PF0 = Pin(160)
PF1 = Pin(161)
PF2 = Pin(162)
PF3 = Pin(163)
PF4 = Pin(164)
PF5 = Pin(165)
PF6 = Pin(166)
PG0 = Pin(192)
PG1 = Pin(193)
PG2 = Pin(194)
PG3 = Pin(195)
PG4 = Pin(196)
PG5 = Pin(197)
PG6 = Pin(198)
PG7 = Pin(199)
PG8 = Pin(200)
PG9 = Pin(201)
PG10 = Pin(202)
PG11 = Pin(203)
PG12 = Pin(204)
PG13 = Pin(205)
PG14 = Pin(206)
PG15 = Pin(207)

# GPADC channel 0 (0 - 1.8V): IIO device 0, channel 0
GPADC0 = 0

i2cPorts = (
    (0, PB3, PB2),
    (0, PD0, PD12),
    (0, PE2, PE3),
    (0, PF2, PF4),
    (0, PG12, PG13),
    (1, PB4, PB5),
    (1, PE0, PE1),
    (1, PG8, PG9),
    (2, PD20, PD21),
    (2, PE4, PE5),
    (2, PE12, PE13),
    (2, PG6, PG7),
    (2, PG14, PG15),
    (3, PB6, PB7),
    (3, PC6, PC7),
    (3, PE6, PE7),
    (3, PG10, PG11),
)

uartPorts = (
    (0, PE2, PE3),
    (0, PF2, PF4),
    (1, PD21, PD22),
    (1, PE10, PE11),
    (1, PG6, PG7),
    (1, PG12, PG13),
    (2, PD1, PD2),
    (2, PE2, PE3),
    (3, PB6, PB7),
    (3, PC6, PC7),
    (3, PD10, PD11),
    (3, PE8, PE9),
    (3, PG0, PG1),
    (3, PG8, PG9),
    (4, PB2, PB3),
    (4, PD7, PD8),
    (4, PE4, PE5),
    (4, PG2, PG3),
    (5, PB4, PB5),
    (5, PD5, PD6),
    (5, PE6, PE7),
    (5, PG4, PG5),
)

spiPorts = (
    (0, PC2, PC4, PC5),
    (1, PD11, PD12, PD13),
)

analogIns = ((GPADC0, 0, 0),)

# PWM controller at 0x2000c00 (pwm-sun8i driver): its pwmchip number depends
# on the probe order, so look it up. A pin is a PWM output once the device
# tree muxes it to its pwm function.
pwmOuts = []
_PWM_CHANNELS = (
    (0, PB5),
    (0, PD16),
    (0, PG12),
    (1, PB6),
    (1, PD17),
    (1, PG6),
    (2, PD18),
    (2, PE8),
    (2, PG13),
    (3, PD19),
    (3, PE9),
    (3, PG10),
    (4, PD20),
    (4, PE10),
    (4, PG5),
    (5, PD21),
    (5, PE13),
    (5, PF6),
    (5, PG4),
    (6, PD9),
    (6, PF4),
    (6, PG1),
    (7, PD22),
    (7, PG0),
)
_pwm_chip = get_pwm_chipid("2000c00.pwm")
if _pwm_chip is not None:
    for _channel, _pin in _PWM_CHANNELS:
        pwmOuts.append(((int(_pwm_chip[3:]), _channel), _pin))
