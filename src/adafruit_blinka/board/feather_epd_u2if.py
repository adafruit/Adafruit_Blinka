# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Pin definitions for the Feather RP2040 ThinkInk with u2if firmware.

Adafruit CircuitPython 6.2.0 on 2021-04-05; Adafruit Feather RP2040 ThinkInk with rp2040
>>> import board
>>> board.
A0              A1              A2              A3
D0              D1              D10             D11
D12             D13             D24             D25
D4              D5              D6              D9
I2C             LED             MISO            MOSI
NEOPIXEL        EPD_BUSY        SCK             SCL
SDA             SPI             TX              UART
EPD_CS          EPD_RESET       EPD_DC          EPD_MOSI
EPD_SCK
"""

from adafruit_blinka.microcontroller.rp2040_u2if import pin

D0 = pin.GP1
D1 = pin.GP0
D4 = pin.GP4
D5 = pin.GP5
D6 = pin.GP6
D9 = pin.GP9
D10 = pin.GP10
D11 = pin.GP11
D12 = pin.GP12
D13 = pin.GP13
D24 = pin.GP24
D25 = pin.GP25

A0 = pin.GP26
A1 = pin.GP27
A2 = pin.GP28
A3 = pin.GP29

LED = pin.GP13

BUTTON = BOOT = pin.GP7

NEOPIXEL = pin.GP21
NEOPIXEL_POWER = pin.GP20

SDA = pin.GP2
SCL = pin.GP3

SCLK = SCK = pin.GP14
MOSI = pin.GP15
MISO = pin.GP8

EPD_BUSY = pin.GP16
EPD_RESET = pin.GP17
EPD_DC = pin.GP18
EPD_CS = pin.GP19
EPD_SCK = pin.GP22
EPD_MOSI = pin.GP23

# access u2if via pin instance to open for specifc VID/PID
# pylint:disable = protected-access
pin.GP0._u2if_open_hid(0x239A, 0x812C)
