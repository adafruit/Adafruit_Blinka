# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`rainbowio` - Provides the `colorwheel()` function
===========================================================
See `CircuitPython:rainbowio` in CircuitPython for more details.
Not supported by all boards.

* Author(s): Kattni Rembor, Carter Nelson
"""


def colorwheel(color_value):
    """
    A colorwheel. ``0`` and ``255`` are red, ``85`` is green, and ``170`` is blue, with the values
    between being the rest of the rainbow.

    :param int color_value: 0-255 of color value to return
    :return: tuple of RGB values
    """
    color_value = int(color_value)
    if color_value < 0 or color_value > 255:
        r = 0
        g = 0
        b = 0
    elif color_value < 85:
        r = int(255 - color_value * 3)
        g = int(color_value * 3)
        b = 0
    elif color_value < 170:
        color_value -= 85
        r = 0
        g = int(255 - color_value * 3)
        b = int(color_value * 3)
    else:
        color_value -= 170
        r = int(color_value * 3)
        g = 0
        b = int(255 - color_value * 3)
    return r << 16 | g << 8 | b
