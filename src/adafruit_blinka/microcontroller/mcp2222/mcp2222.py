# SPDX-FileCopyrightText: 2026 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Shared USB connection to the MCP2222."""

import atexit

from pymcp2222 import MCP2222Device

mcp2222 = MCP2222Device()
mcp2222.open()
atexit.register(mcp2222.close)
