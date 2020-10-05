import time
import sys
import board
import busio
import hid

from adafruit_blinka.microcontroller.mcp2221.mcp2221 import mcp2221 as _mcp2221
from adafruit_blinka.microcontroller.mcp2221.mcp2221 import MCP2221 as _MCP2221
from adafruit_blinka.microcontroller.mcp2221.i2c import I2C as _MCP2221I2C


class MCP2221(_MCP2221): 
    def __init__(self, address):
        self._hid = hid.device()
        self._hid.open_path(address)
        print("Connected to "+str(address))
        self._gp_config = [0x07] * 4  # "don't care" initial value
        for pin in range(4):
            self.gp_set_mode(pin, self.GP_GPIO)  # set to GPIO mode
            self.gpio_set_direction(pin, 1)  # set to INPUT


class MCP2221I2C(_MCP2221I2C):
    def __init__(self, mcp2221, *, frequency=1000000):
        self._mcp2221 = mcp2221
        self._mcp2221.i2c_configure(frequency)


class I2C(busio.I2C):
    def __init__(self, mcp2221_i2c, *, frequency=1000000):
        self._i2c = mcp2221_i2c


def temp_c(data):
    value = data[0] << 8 | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp


while True:
    i2c.writeto(0x18, bytes([0x05]), stop=False)
    result = bytearray(2)
    i2c.readfrom_into(0x18, result)
    print(temp_c(result))
    time.sleep(0.5)
