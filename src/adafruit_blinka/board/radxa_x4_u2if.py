# SPDX-FileCopyrightText: 2025 Bernhard Bablok
#
# Copied and adapted from pico_u2if.py
# Copyright: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Raspberry Pi Pico running u2if firmware"""
from adafruit_blinka.microcontroller.rp2040_u2if import pin

# Pico names
GP0 = pin.GP0
GP1 = pin.GP1
GP2 = pin.GP2
GP3 = pin.GP3
GP4 = pin.GP4
GP5 = pin.GP5
GP6 = pin.GP6
GP7 = pin.GP7
GP8 = pin.GP8
GP9 = pin.GP9
GP10 = pin.GP10
GP11 = pin.GP11
GP12 = pin.GP12
GP13 = pin.GP13
GP14 = pin.GP14
GP15 = pin.GP15
GP16 = pin.GP16
GP17 = pin.GP17
GP18 = pin.GP18
GP19 = pin.GP19
GP20 = pin.GP20
GP21 = pin.GP21
GP22 = pin.GP22
GP23 = pin.GP23
GP24 = pin.GP24
GP25 = pin.GP25
GP26 = pin.GP26
GP27 = pin.GP27
GP28 = pin.GP28
GP29 = pin.GP29

# Pi names left side (top down)
GPIO2 = GP28
GPIO3 = GP29

GPIO4 = GP4
GPIO17 = GP5
GPIO27 = GP6
GPIO22 = GP3

GPIO10 = GP11
GPIO9 = GP8
GPIO11 = GP10

GPIO0 = GP16
GPIO5 = GP7
GPIO6 = GP12
GPIO13 = GP13
GPIO19 = GP15
GPIO26 = GP14

# right side (top down)
GPIO14 = GP20
GPIO15 = GP21
GPIO18 = GP23

GPIO23 = GP22
GPIO24 = GP27

GPIO25 = GP24
GPIO8 = GP9
GPIO7 = GP18
GPIO1 = GP17

GPIO12 = GP19

GPIO16 = GP26
GPIO20 = GP2
GPIO21 = GP25

# specials (INT: internal connection to N100-chip, EXT: on GPIO-pins)
UART_TX_INT = GP0
UART_RX_INT = GP1
UART_RX_EXT = GP20  # GPIO14
UART_RX_EXT = GP21  # GPIO15

ADC0 = GP26
ADC1 = GP27
ADC2 = GP28
ADC3 = GP29

PWM0 = GPIO12
PWM1 = GPIO13

# Pi defaults (I2C0 is also mapped to the ID-pins GPIO0/GPIO1 aka GP16/GP17)
SDA = SDA0 = GP28  # GPIO2
SCL = SCL0 = GP29  # GPIO3

# other choices have more conflicts
SDA1 = GP18
SCL1 = GP19

# Pico-SPI0 (Radxa-X4 does not map Pi-SPI1)
SCLK0 = SCK0 = GP6
MOSI0 = GP3
MISO0 = GP4
CE0 = GPIO8
CE1 = GPIO7

# Pi (SPI0) defaults (Radxa-X4 maps Pi-SPI0 to Pico-SPI1)
SCLK = SCK = SCLK1 = SCK1 = GP10
MOSI = MOSI1 = GP11
MISO = MISO1 = GP8

# access u2if via pin instance to open for specifc VID/PID
# pylint:disable = protected-access
pin.GP0._u2if_open_hid(0xCAFF, 0x4005)
