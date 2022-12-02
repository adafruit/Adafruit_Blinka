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


def native(f):
    "Emulate making a native"
    return f


def viper(f):
    "User is attempting to use a viper code emitter"
    raise SyntaxError("invalid micropython decorator")


def asm_thumb(f):
    "User is attempting to use an inline assembler"
    raise SyntaxError("invalid micropython decorator")
