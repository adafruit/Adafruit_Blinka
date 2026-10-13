# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`micropython` - MicroPython Specific Decorator Functions
========================================================

* Author(s): cefn
"""

from typing import Callable, TypeVar, Any, Literal, NoReturn, overload

Fun = TypeVar("Fun", bound=Callable[..., Any])
T = TypeVar("T")

def const(x: T) -> T:
    "Emulate making a constant"

@overload
def native(f: Fun) -> Fun:
    "Emulate making a native"

@overload
def native(*, optional: bool = ...) -> Callable[[Fun], Fun]:
    "Emulate making a native"

@overload
def viper(f: Fun) -> NoReturn:
    "User is attempting to use a viper code emitter"

@overload
def viper(*, optional: Literal[True]) -> Callable[[Fun], Fun]:
    "Viper code that also runs as plain Python"

@overload
def viper(*, optional: Literal[False] = ...) -> NoReturn:
    "User is attempting to use a viper code emitter"

def asm_thumb(f: Fun) -> NoReturn:
    "User is attempting to use an inline assembler"
