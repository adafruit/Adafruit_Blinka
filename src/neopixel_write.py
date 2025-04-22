# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`neopixel_write` - NeoPixel precision timed writing support
===========================================================

See `CircuitPython:neopixel_write` in CircuitPython for more details.
Currently supported on Raspberry Pi only.

* Author(s): ladyada
"""
# pylint: disable=too-many-boolean-expressions, ungrouped-imports
import sys

from adafruit_blinka.agnostic import detector

if detector.board.any_raspberry_pi:
    if detector.board.any_raspberry_pi_5_board:
        import adafruit_raspberry_pi5_neopixel_write as _neopixel
    else:
        from adafruit_blinka.microcontroller.bcm283x import neopixel as _neopixel
elif detector.board.pico_u2if:
    from adafruit_blinka.microcontroller.rp2040_u2if import neopixel as _neopixel
elif detector.board.OS_AGNOSTIC_BOARD:
    from adafruit_blinka.microcontroller.generic_agnostic_board import (
        neopixel as _neopixel,
    )
elif (
    detector.board.feather_u2if
    or detector.board.feather_can_u2if
    or detector.board.feather_epd_u2if
    or detector.board.feather_rfm_u2if
    or detector.board.qtpy_u2if
    or detector.board.itsybitsy_u2if
    or detector.board.macropad_u2if
    or detector.board.qt2040_trinkey_u2if
    or detector.board.kb2040_u2if
):
    from adafruit_blinka.microcontroller.rp2040_u2if import neopixel as _neopixel
elif "sphinx" in sys.modules:
    pass
else:
    raise NotImplementedError("Board not supported")


def neopixel_write(gpio, buf):
    """Write buf out on the given DigitalInOut."""
    return _neopixel.neopixel_write(gpio, buf)
