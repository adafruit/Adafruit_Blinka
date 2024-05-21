# SPDX-FileCopyrightText: 2024 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""I2C Class for Generic Agnostic Board"""
from random import randint

# from .generic_agnostic_board.pin import generic_agnostic_board


class I2C:
    """Custom I2C Class for a Generic Agnostic Board"""

    def __init__(self, *, frequency=100000):
        # self._generic_agnostic_board = generic_agnostic_board
        self.freq = frequency

    @staticmethod
    def scan():
        """Mocks an I2C scan and returns a list of 3 randomly generated
        I2C addresses from 0x0 to 0x79.
        """
        # Generate a list of 3 randomly generated addresses from 0x0 to 0x79
        address_list = []
        for _ in range(3):
            address_list.append(randint(0x0, 0x79))
        return address_list
