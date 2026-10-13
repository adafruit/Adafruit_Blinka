# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`micropython` - MicroPython Specific Decorator Functions
========================================================

* Author(s): cefn
"""

from typing import Any, Callable, Literal, NoReturn, Optional, TypeVar, Union, overload

Fun = TypeVar("Fun", bound=Callable[..., Any])
T = TypeVar("T")


def const(x: T) -> T:
    "Emulate making a constant"
    return x


@overload
def native(f: Fun) -> Fun:
    "Emulate making a native"


@overload
def native(*, optional: bool = ...) -> Callable[[Fun], Fun]:
    "Emulate making a native"


def native(
    f: Optional[Fun] = None,
    *,
    optional: bool = False  # pylint: disable=unused-argument
) -> Union[Fun, Callable[[Fun], Fun]]:
    """Emulate making a native function. The function runs as plain Python."""
    if f is None:
        return lambda function: function
    return f


@overload
def viper(f: Fun) -> NoReturn:
    "User is attempting to use a viper code emitter"


@overload
def viper(*, optional: Literal[True]) -> Callable[[Fun], Fun]:
    "Viper code that also runs as plain Python"


@overload
def viper(*, optional: Literal[False] = ...) -> NoReturn:
    "User is attempting to use a viper code emitter"


def viper(f: Optional[Fun] = None, *, optional: bool = False) -> Callable[[Fun], Fun]:
    """
    The viper code emitter is not available. With ``optional=True`` the
    function runs as plain Python, as it does on a board without viper.
    """
    if f is None and optional:
        return lambda function: function
    raise SyntaxError("invalid micropython decorator")


def asm_thumb(f: Fun) -> NoReturn:
    "User is attempting to use an inline assembler"
    raise SyntaxError("invalid micropython decorator")
