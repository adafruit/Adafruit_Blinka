# SPDX-FileCopyrightText: 2023 Carter Nelson for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Pin definitions for the KB2040 with u2if firmware.

Adafruit CircuitPython 8.2.0 on 2023-07-05; Adafruit KB2040 with rp2040
>>> import board
>>> board.
A0              A1              A2              A3
BUTTON          CLK             D0              D1
D10             D11             D12             D13
D2              D3              D4              D5
D6              D7              D8              D9
I2C             MISO            MOSI            NEOPIXEL
RX              SCK             SCL             SDA
SPI             STEMMA_I2C      TX              UART
board_id
"""

from adafruit_blinka.microcontroller.rp2040_u2if import pin

D0 = TX = pin.GP0
D1 = RX = pin.GP1
D2 = pin.GP2
D3 = pin.GP3
D4 = pin.GP4
D5 = pin.GP5
D6 = pin.GP6
D7 = pin.GP7
D8 = pin.GP8
D9 = pin.GP9
D10 = pin.GP10
D11 = pin.GP11
D12 = pin.GP12
D13 = pin.GP13

A0 = pin.GP26
A1 = pin.GP27
A2 = pin.GP28
A3 = pin.GP29

BUTTON = pin.GP11

NEOPIXEL = pin.GP17

SDA = pin.GP12
SCL = pin.GP13

SCLK = pin.GP18
MOSI = pin.GP19
MISO = pin.GP20


# access u2if via pin instance to open for specifc VID/PID
# pylint:disable = protected-access
pin.GP0._u2if_open_hid(0x239A, 0x0105)
