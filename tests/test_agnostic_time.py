# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Time-shim tests with inert MicroPython modules and no board detection."""

import importlib.util
import sys
import time
from collections import namedtuple
from pathlib import Path
from types import ModuleType

import pytest

import adafruit_blinka

# Pytest supplies the named fixtures.
# pylint: disable=redefined-outer-name

SOURCE = Path(__file__).parents[1] / "src/adafruit_blinka/agnostic/time.py"
FIELDS = (
    "tm_year",
    "tm_mon",
    "tm_mday",
    "tm_hour",
    "tm_min",
    "tm_sec",
    "tm_wday",
    "tm_yday",
    "tm_isdst",
)


def load_time_shim(monkeypatch, implementation):
    """Select the interpreter branch without importing a real platform detector."""
    agnostic = ModuleType("adafruit_blinka.agnostic")
    agnostic.implementation = implementation
    monkeypatch.setitem(sys.modules, "adafruit_blinka.agnostic", agnostic)
    monkeypatch.setattr(adafruit_blinka, "agnostic", agnostic, raising=False)
    spec = importlib.util.spec_from_file_location("_test_agnostic_time", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def micropython_time(monkeypatch):
    """Use the documented namedtuple contract and a fixed, inert tick counter."""
    utime = ModuleType("utime")
    utime.sleep = lambda _seconds: None
    utime.ticks_ms = lambda: 0
    utime.ticks_diff = lambda current, previous: current - previous
    ucollections = ModuleType("ucollections")
    ucollections.namedtuple = namedtuple
    monkeypatch.setitem(sys.modules, "utime", utime)
    monkeypatch.setitem(sys.modules, "ucollections", ucollections)
    return load_time_shim(monkeypatch, "micropython")


@pytest.mark.parametrize("container", [tuple, list], ids=["tuple", "list"])
@pytest.mark.parametrize(
    "values, expected",
    [
        (
            (2026, 10, 20, 12, 34, 56, 1, 293, 1),
            (2026, 10, 20, 12, 34, 56, 1, 293, 1),
        ),
        (
            (2026, 10, 20, 12, 34, 56, 1, 293),
            (2026, 10, 20, 12, 34, 56, 1, 293, -1),
        ),
        ((2026, 10, 20), (2026, 10, 20, 0, 0, 0, -1, -1, -1)),
    ],
    ids=["all-fields", "micropython-eight-fields", "adapter-defaults"],
)
def test_struct_time_returns_ordered_named_fields(
    micropython_time, container, values, expected
):
    """Return the constructed tuple, retaining explicit values and shim defaults."""
    result = micropython_time.struct_time(container(values))
    assert isinstance(result, tuple)
    assert len(result) == 9
    assert tuple(result) == expected
    assert tuple(getattr(result, field) for field in FIELDS) == expected


@pytest.mark.parametrize("length", [0, 2, 10])
def test_invalid_argument_count_still_raises(micropython_time, length):
    """Returning the value must not change the existing argument-count checks."""
    with pytest.raises(TypeError):
        micropython_time.struct_time((0,) * length)


def test_circuitpython_branch_still_reexports_native_time(monkeypatch):
    """Exercise passthrough using host time, not a real CircuitPython runtime."""
    module = load_time_shim(monkeypatch, "circuitpython")
    assert module.struct_time is time.struct_time
    assert module.monotonic is time.monotonic
    assert module.sleep is time.sleep
