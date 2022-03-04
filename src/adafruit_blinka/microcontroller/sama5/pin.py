# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Atmel SAMA5 pin names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PD23 = Pin(119)
AD4 = PD23
PD21 = Pin(117)
AD2 = PD21
PD20 = Pin(116)
AD1 = PD20
PD24 = Pin(120)
AD5 = PD24
PD22 = Pin(118)
AD3 = PD22
PD19 = Pin(115)
AD0 = PD19
PA14 = Pin(14)
SPI0_SCLK = PA14
PA15 = Pin(15)
SPI0_MOSI = PA15
PA16 = Pin(16)
SPI0_MISO = PA16
PD2 = Pin(98)
UART1_RX = PD2
PD3 = Pin(99)
UART1_TX = PD3

PD13 = Pin(109)
PD31 = Pin(127)
PB0 = Pin(32)
PWM1 = PB0
PB7 = Pin(39)
PWM3 = PB7
PB1 = Pin(33)
PWML1 = PB1
PB5 = Pin(37)
PWM2 = PB5
PB3 = Pin(35)
PC0 = Pin(64)
TWI0_SCL = PC0
PB31 = Pin(63)
TWI0_SDA = PB31

i2cPorts = ((0, TWI0_SCL, TWI0_SDA),)
# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),)
# ordered as uartId, txId, rxId
uartPorts = ((1, UART1_TX, UART1_RX),)
# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = (
    ((0, 1), PWM1),
    ((0, 2), PWM2),
    ((0, 3), PWM3),
)
