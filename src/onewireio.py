# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`onewireio` - 1-wire bus protocol
=================================================

See `CircuitPython:onewireio` in CircuitPython for more details.

* Author(s): cefn
"""

# pylint: disable=import-outside-toplevel,too-many-branches,too-many-statements
# pylint: disable=too-many-arguments,too-many-function-args,too-many-return-statements


class OneWire:
    """
    Stub class for OneWire, which is currently not implemented
    """

    def __init__(self, pin):
        raise NotImplementedError("OneWire has not been implemented")

    def deinit(self):
        """
        Deinitialize the OneWire bus and release any hardware resources for reuse.
        """
        raise NotImplementedError("OneWire has not been implemented")

    def reset(self):
        """
        Reset the OneWire bus and read presence
        """
        raise NotImplementedError("OneWire has not been implemented")

    def read_bit(self):
        """
        Read in a bit
        """
        raise NotImplementedError("OneWire has not been implemented")

    def write_bit(self, value):
        """
        Write out a bit based on value.
        """
        raise NotImplementedError("OneWire has not been implemented")
