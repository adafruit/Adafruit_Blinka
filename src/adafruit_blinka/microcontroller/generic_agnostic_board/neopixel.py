# SPDX-FileCopyrightText: 2024 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""NeoPixel write mocks for a generic board."""


# pylint: disable=unused-argument
def neopixel_write(gpio, buf):
    """Mocks a neopixel_write function"""
    # pad output buffer from 3 bpp to 4 bpp
    buffer = []
    for i in range(0, len(buf), 3):
        buffer.append(0)
        buffer.append(buf[i + 2])
        buffer.append(buf[i + 1])
        buffer.append(buf[i])

    # then, do nothing
