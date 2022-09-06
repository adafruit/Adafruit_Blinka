# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`micropython` - MicroPython Specific Decorator Functions
========================================================

* Author(s): cefn
"""

from typing import Callable, TypeVar, Any, NoReturn

Fun = TypeVar("Fun", bound=Callable[..., Any])

def const(x: int) -> int:
    "Emulate making a constant"

def native(f: Fun) -> Fun:
    "Emulate making a native"

def viper(f: Fun) -> NoReturn:
    "User is attempting to use a viper code emitter"

def asm_thumb(f: Fun) -> NoReturn:
    "User is attempting to use an inline assembler"
