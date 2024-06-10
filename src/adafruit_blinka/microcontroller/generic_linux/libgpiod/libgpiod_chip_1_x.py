# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""A Chip class for use with libgpiod 1.x."""
import gpiod


# pylint: disable=too-many-branches,too-many-statements
class Chip:
    """Abstraction for handling all breaking changes over the lifecycle of gpiod"""

    _CONSUMER = "adafruit_blinka"

    id: str = None
    num_lines: int

    def __init__(self, chip_id: str):
        self.id = chip_id
        if hasattr(gpiod, "Chip"):
            self._chip = gpiod.Chip(self.id)
        else:
            self._chip = gpiod.chip(self.id)

        if callable(self._chip.num_lines):
            self.num_lines = self._chip.num_lines()
        else:
            self.num_lines = self.num_lines

    def __repr__(self):
        return self.id

    def __eq__(self, other):
        return self.id == other
