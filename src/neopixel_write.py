"""
`neopixel_write` - NeoPixel precision timed writing support
=================================================

See `CircuitPython:neopixel_write` in CircuitPython for more details.

* Author(s): ladyada
"""

import sys

from adafruit_blinka.agnostic import board_name
import adafruit_platformdetect.board as ap_board

if board_name in (ap_board.RASPBERRY_PI_2B, ap_board.RASPBERRY_PI_3B, ap_board.RASPBERRY_PI_B_PLUS):
    from adafruit_blinka.microcontroller.bcm283x import neopixel as _neopixel
elif "sphinx" in sys.modules:
    pass
else:
    raise NotImplementedError("Board not supported")


def neopixel_write(gpio, buf):
    """Write buf out on the given DigitalInOut."""
    return _neopixel.neopixel_write(gpio, buf)
