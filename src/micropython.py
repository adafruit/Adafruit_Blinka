# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`micropython` - MicroPython Specific Decorator Functions
========================================================

* Author(s): cefn
"""


def const(x):
    "Emulate making a constant"
    return x


def native(f=None, *, optional=False):  # pylint: disable=unused-argument
    """Emulate making a native function. The function runs as plain Python."""
    if f is None:
        return lambda function: function
    return f


def viper(f=None, *, optional=False):
    """
    The viper code emitter is not available. With ``optional=True`` the
    function runs as plain Python, as it does on a board without viper.
    """
    if f is None and optional:
        return lambda function: function
    raise SyntaxError("invalid micropython decorator")


def asm_thumb(f):
    "User is attempting to use an inline assembler"
    raise SyntaxError("invalid micropython decorator")
