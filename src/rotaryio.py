# SPDX-FileCopyrightText: 2025 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`rotaryio` - Support for reading rotation sensors
===========================================================
See `CircuitPython:rotaryio` in CircuitPython for more details.

* Author(s): Melissa LeBlanc-Williams
"""

from adafruit_blinka.agnostic import detector

# pylint: disable=unused-import

# Import any board specific modules here
if detector.board.any_raspberry_pi_5_board:
    from adafruit_blinka.microcontroller.bcm283x.rotaryio import IncrementalEncoder
elif detector.board.any_embedded_linux:
    # fall back to the generic linux implementation
    from adafruit_blinka.microcontroller.generic_linux.rotaryio import (
        IncrementalEncoder,
    )
else:
    # For non-Linux Boards, threading likely will work in the same way
    raise NotImplementedError("Board not supported")
