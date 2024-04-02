# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Chip Definition for MCP2221"""


class MCP2221:
    """MCP2221 Device Class Definition"""

    def __init__(self):
        pass  # This is a "fake" implementation

    def __del__(self):
        # try to close the device before destroying the instance
        return

    # pylint: enable=unused-argument


mcp2221 = MCP2221()
