# SPDX-FileCopyrightText: 2026 Mikey Sklar for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import pytest

import micropython


def add(a, b):
    return a + b


def test_native():
    assert micropython.native(add) is add
    assert micropython.native(optional=True)(add) is add
    assert micropython.native(optional=False)(add) is add


def test_viper():
    assert micropython.viper(optional=True)(add) is add
    with pytest.raises(SyntaxError):
        micropython.viper(add)
    with pytest.raises(SyntaxError):
        micropython.viper(optional=False)
