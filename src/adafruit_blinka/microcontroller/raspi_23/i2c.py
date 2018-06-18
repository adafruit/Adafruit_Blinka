import smbus
import time


class I2C:

    _i2c_bus = None
    def __init__(self, bus_num=0):
        i2c_bus = smbus.SMBus(bus_num)
