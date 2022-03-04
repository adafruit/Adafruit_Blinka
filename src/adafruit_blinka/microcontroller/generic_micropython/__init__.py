# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Genereic Pin class for use with MicroPython boards"""
from adafruit_blinka import Enum


class Pin(Enum):
    """
    Identifies an IO pin on the microcontroller.

    They are fixed by the hardware so they cannot be constructed on demand. Instead, use board or
    microcontroller.pin to reference the desired pin.
    """

    def __init__(self, pin_id):
        """Identifier for pin, referencing platform-specific pin id"""
        self.id = pin_id

    def __repr__(self):
        # pylint: disable=import-outside-toplevel, cyclic-import
        import board
        import microcontroller.pin

        for key in dir(board):
            if getattr(board, key) is self:
                return "board.{}".format(key)
        # pylint: enable=import-outside-toplevel, cyclic-import

        for key in dir(microcontroller.pin):
            if getattr(microcontroller.pin, key) is self:
                return "microcontroller.pin.{}".format(key)
        return repr(self)
