"""
`neopixel_write` - NeoPixel precision timed writing support
=================================================

See `CircuitPython:neopixel_write` in CircuitPython for more details.

* Author(s): ladyada
"""

import sys

from adafruit_blinka.agnostic import board_id

if board_id == "raspi_2" or board_id == "raspi_3":
    from adafruit_blinka.microcontroller.raspi_23 import neopixel as _neopixel
elif "sphinx" in sys.modules:
    pass
else:
    raise NotImplementedError("Board not supported")


def neopixel_write(gpio, buf):
    """Write buf out on the given DigitalInOut."""
    return _neopixel.neopixel_write(gpio, buf)
