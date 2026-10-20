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
    A colorwheel. ``0`` and ``255`` are red, ``85`` is green, and ``170`` is blue,
    with the values between being the rest of the rainbow. Nonnegative finite
    hues repeat every 256, and fractional hues interpolate between colors.

    :param float color_value: Hue, normally in the range 0-255
    :return: RGB color packed into a 24-bit integer
    """
    if not isinstance(color_value, (bool, int, float)) and not hasattr(
        color_value, "__float__"
    ):
        raise TypeError("color_value must be a number")
    color_value = float(color_value)
    if color_value < 0:
        return 0
    color_value %= 256
    if color_value < 85:
        shift1, shift2 = 8, 16
    elif color_value < 170:
        color_value -= 85
        shift1, shift2 = 0, 8
    else:
        color_value -= 170
        shift1, shift2 = 16, 0
    channel = min(int(color_value * 3), 255)
    return (channel << shift1) | ((255 - channel) << shift2)
