# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Platform agnostic time implementation"""

from adafruit_blinka import agnostic

# We intentionally are patching into this namespace so skip the wildcard check.
# pylint: disable=unused-wildcard-import,wildcard-import

if agnostic.implementation == "circuitpython":
    from time import *
elif agnostic.implementation == "micropython":
    import utime
    from utime import sleep

    from ucollections import namedtuple

    _struct_time = namedtuple(
        "struct_time",
        (
            "tm_year",
            "tm_mon",
            "tm_mday",
            "tm_hour",
            "tm_min",
            "tm_sec",
            "tm_wday",
            "tm_yday",
            "tm_isdst",
        ),
    )

    # pylint: disable=too-many-arguments
    def _marshal_time(
        tm_year,
        tm_mon,
        tm_mday,
        tm_hour=0,
        tm_min=0,
        tm_sec=0,
        tm_wday=-1,
        tm_yday=-1,
        tm_isdst=-1,
    ):
        """Construct struct_time with default values."""
        _struct_time(
            tm_year,
            tm_mon,
            tm_mday,
            tm_hour,
            tm_min,
            tm_sec,
            tm_wday,
            tm_yday,
            tm_isdst,
        )

    def struct_time(time_tuple):
        """Create a struct_time"""
        return _marshal_time(*time_tuple)

    # pylint: disable=invalid-name
    _total_ms = 0
    _prev_ticks_ms = utime.ticks_ms()

    def monotonic():
        """A monotonically increasing time in seconds. No defined start time."""
        # Assumes that monotonic is called more frequently than the wraparound of micropython's
        # utime.ticks_ms()
        global _prev_ticks_ms, _total_ms  # pylint: disable=global-statement
        ticks_ms = utime.ticks_ms()
        _total_ms += utime.ticks_diff(ticks_ms, _prev_ticks_ms)
        _prev_ticks_ms = ticks_ms
        return _total_ms * 0.001
