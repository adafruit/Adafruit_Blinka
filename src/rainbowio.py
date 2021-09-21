"""
`rainbowio` - Provides the `colorwheel()` function
===========================================================
See `CircuitPython:rainbowio` in CircuitPython for more details.
Not supported by all boards.

* Author(s): Kattni Rembor
"""


def colorwheel(color_value):
    """
    A colorwheel. ``0`` and ``255`` are red, ``85`` is green, and ``170`` is blue, with the values
    between being the rest of the rainbow.

    :param int color_value: 0-255 of color value to return
    :return: tuple of RGB values
    """
    if color_value < 0 or color_value > 255:
        return 0, 0, 0
    if color_value < 85:
        return 255 - color_value * 3, color_value * 3, 0
    if color_value < 170:
        color_value -= 85
        return 0, 255 - color_value * 3, color_value * 3
    color_value -= 170
    return color_value * 3, 0, 255 - color_value * 3
