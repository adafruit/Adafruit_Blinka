from adafruit_blinka import agnostic
if agnostic.implementation == "circuitpython":
    from time import *
elif agnostic.implementation == "micropython":
    import utime
    from utime import sleep

    from ucollections import namedtuple
    _struct_time = namedtuple("struct_time", ("tm_year", "tm_mon", "tm_mday", "tm_hour", "tm_min", "tm_sec", "tm_wday", "tm_yday", "tm_isdst"))

    def marshal_time(tm_year, tm_mon, tm_mday, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=-1, tm_yday=-1, tm_isdst=-1):
        _struct_time(tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)

    def struct_time(t):
        return marshal_time(*t)

    total_ms = 0
    prev_ticks_ms = utime.ticks_ms()
    def monotonic():
        """
        Assumes that monotonic is called more frequently than the wraparound of micropython's utime.ticks_ms()
        """
        global prev_ticks_ms, total_ms
        ticks_ms = utime.ticks_ms()
        total_ms += utime.ticks_diff(ticks_ms, prev_ticks_ms)
        prev_ticks_ms = ticks_ms
        return total_ms * 0.001