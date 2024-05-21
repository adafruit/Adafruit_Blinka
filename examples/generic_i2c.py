import pytest
import busio
from board import *


def test_i2c_scan_random():
    i2c = busio.I2C(SCL, SDA)
    i2c.try_lock()
    addr_list = i2c.scan()
    assert len(addr_list) == 3
    for addr in addr_list:
        assert addr >= 0x0 and addr <= 0x79
    i2c.unlock()
    i2c.deinit()
