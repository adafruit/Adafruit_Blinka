from time import sleep

from ucollections import namedtuple
_struct_time = namedtuple("struct_time", ("tm_year", "tm_mon", "tm_mday", "tm_hour", "tm_min", "tm_sec", "tm_wday", "tm_yday", "tm_isdst"))

def marshal_time(tm_year, tm_mon, tm_mday, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=-1, tm_yday=-1, tm_isdst=-1):
    _struct_time(tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst)

def struct_time(t):
    return marshal_time(*t)

#TODO implement time.monotonic based on ticks_ms
