# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the QT2040 Trinkey with u2if firmware."""

from adafruit_blinka.microcontroller.rp2040_u2if import pin

BUTTON = pin.GP12

SCL = pin.GP17
SDA = pin.GP16

NEOPIXEL = pin.GP27

# access u2if via pin instance to open for specifc VID/PID
# pylint:disable = protected-access
pin.GP0._u2if_open_hid(0x239A, 0x0109)
