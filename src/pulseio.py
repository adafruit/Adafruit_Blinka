# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`pulseio` - Pulse Width Modulation input and output control
===========================================================
See `CircuitPython:pulseio` in CircuitPython for more details.
Not supported by all boards.

* Author(s): Melissa LeBlanc-Williams
"""

import sys

from adafruit_blinka.agnostic import detector

# pylint: disable=unused-import

if detector.board.any_raspberry_pi:
    from adafruit_blinka.microcontroller.bcm283x.pulseio.PulseIn import PulseIn
elif "sphinx" in sys.modules:
    pass
else:
    raise NotImplementedError("pulseio not supported for this board.")
