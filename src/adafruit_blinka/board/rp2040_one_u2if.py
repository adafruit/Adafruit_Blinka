# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Pin definitions for the Waveshare RP2040 One with u2if firmware.

Adafruit CircuitPython; Waveshare RP2040 One with rp2040
>>> import board
>>> board.
A0              A1              A2              A3
D2              D3              D10             D11
D12             D13             D14             D15
D17             D18             D19             D20
D21             D22             D23             D24
D25             D9              I2C             MISO
MOSI            NEOPIXEL        RX              SCK
SCL             SDA             SPI             TX
UART
"""

from adafruit_blinka.microcontroller.rp2040_u2if import pin

D2 = pin.GP2
D3 = pin.GP3
D9 = pin.GP9
D10 = pin.GP10
D11 = pin.GP11
D12 = pin.GP12
D13 = pin.GP13
D14 = pin.GP14
D15 = pin.GP15
D17 = pin.GP17
D18 = pin.GP18
D19 = pin.GP19
D20 = pin.GP20
D21 = pin.GP21
D22 = pin.GP22
D23 = pin.GP23
D24 = pin.GP24
D25 = pin.GP25

A0 = pin.GP26
A1 = pin.GP27
A2 = pin.GP28
# A3 = pin.GP29 # not currently supported in firmware

NEOPIXEL = pin.GP16

TX = pin.GP0
RX = pin.GP1

SCL = pin.GP5
SDA = pin.GP4

SCLK = SCK = pin.GP6
MOSI = pin.GP7
MISO = pin.GP8

# access u2if via pin instance to open for specifc VID/PID
# pylint:disable = protected-access
pin.GP0._u2if_open_hid(0x2E8A, 0x103A)
