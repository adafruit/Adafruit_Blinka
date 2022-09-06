# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`micropython` - MicroPython Specific Decorator Functions
========================================================

* Author(s): cefn
"""

from typing import Callable, TypeVar, Any

Fun = TypeVar("Fun", bound=Callable[..., Any])


def const(x: int) -> int:
    "Emulate making a constant"
    return x


def native(f: Fun) -> Fun:
    "Emulate making a native"
    return f


def viper(f: Fun) -> None:
    "User is attempting to use a viper code emitter"
    raise SyntaxError("invalid micropython decorator")


def asm_thumb(f: Fun) -> None:
    "User is attempting to use an inline assembler"
    raise SyntaxError("invalid micropython decorator")
