# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""I2C Class for MCP2221"""
import random
from .fake_mcp2221 import mcp2221


class I2C:
    """Custom I2C Class for MCP2221"""

    def __init__(self, *, frequency=100000):
        self._mcp2221 = mcp2221
        self._freq = frequency

    @staticmethod
    def scan(address_list=None):
        """Mocks an I2C scan.
        If address_list is not provided, this function returns a
        list of 3 randomly generated I2C addresses from 0x0 to 0x79.
        For a stimulus-driven test: If address_list is provided,
        this function returns the provided address_list.
        """
        if address_list is None:
            # Generate a list of 3 randomly generated addresses from 0x0 to 0x79
            address_list = []
            for _ in range(3):
                address_list.append(random.randint(0x0, 0x79))
            return address_list
        return address_list
