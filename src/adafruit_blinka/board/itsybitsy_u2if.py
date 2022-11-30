# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Pin definitions for the ItsyBitsy RP2040 with u2if firmware.

Adafruit CircuitPython 6.2.0 on 2021-04-05; Adafruit ItsyBitsy RP2040 with rp2040
>>> import board
>>> board.
A0              A1              A2              A3
BUTTON          D0              D1              D10
D11             D12             D13             D2
D24             D25             D3              D4
D5              D7              D9              I2C
LED             MISO            MOSI            NEOPIXEL
NEOPIXEL_POWER  RX              SCK             SCL
SDA             SPI             TX              UART
"""


from adafruit_blinka.microcontroller.rp2040_u2if import pin

D0 = pin.GP1
D1 = pin.GP0
D2 = pin.GP12
D3 = pin.GP5
D4 = pin.GP4
D5 = pin.GP14
D7 = pin.GP6
D9 = pin.GP7
D10 = pin.GP8
D11 = pin.GP9
D12 = pin.GP10
D13 = pin.GP11
D24 = pin.GP24
D25 = pin.GP25

A0 = pin.GP26
A1 = pin.GP27
A2 = pin.GP28
# A3 = pin.GP29 # not currently supported in firmware

SCL = pin.GP3
SDA = pin.GP2

SCLK = SCK = pin.GP18
MOSI = pin.GP19
MISO = pin.GP20

NEOPIXEL = pin.GP17
NEOPIXEL_POWER = pin.GP16

BUTTON = pin.GP13

# access u2if via pin instance to open for specifc VID/PID
# pylint:disable = protected-access
pin.GP0._u2if_open_hid(0x239A, 0x00FD)
