# SPDX-FileCopyrightText: 2024 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Chip Definition for a generic, os-agnostic, board."""


class GENERIC_AGNOSTIC_BOARD:
    """Generic Agnostic Board Device Class Definition"""

    def __init__(self):
        pass  # This implementation is for a generic board, no initialization is required

    def __del__(self):
        # try to close the device before destroying the instance
        return

    # pylint: enable=unused-argument


generic_agnostic_board = GENERIC_AGNOSTIC_BOARD()
