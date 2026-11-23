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
from adafruit_blinka.importing import (
    check_platform_dependency,
    raise_for_missing_platform_dependency,
)


def _load_raspberry_pi_backend():
    """Resolve the Pi backend at first use without installing packages."""
    try:
        if detector.board.any_raspberry_pi_5_board:
            check_platform_dependency("adafruit_raspberry_pi5_neopixel_write")
            import adafruit_raspberry_pi5_neopixel_write as backend
        else:
            check_platform_dependency("_rpi_ws281x")
            from adafruit_blinka.microcontroller.bcm283x import neopixel as backend
    except ModuleNotFoundError as backend_error:
        raise_for_missing_platform_dependency(backend_error)
    return backend


try:
    if detector.board.any_raspberry_pi:
        _neopixel = None
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
except ModuleNotFoundError as error:
    raise_for_missing_platform_dependency(error)


def neopixel_write(gpio, buf):
    """Write buf out on the given DigitalInOut."""
    global _neopixel  # pylint: disable=global-statement
    if _neopixel is None:
        _neopixel = _load_raspberry_pi_backend()
    return _neopixel.neopixel_write(gpio, buf)
