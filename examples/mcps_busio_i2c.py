# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import time
import hid
import busio

from adafruit_blinka.microcontroller.mcp2221.mcp2221 import mcp2221 as _mcp2221
from adafruit_blinka.microcontroller.mcp2221.mcp2221 import MCP2221 as _MCP2221
from adafruit_blinka.microcontroller.mcp2221.i2c import I2C as _MCP2221I2C

MLXADDR = 0x33
ADDRID1 = 0x2407


class MCP2221(_MCP2221):  # pylint: disable=too-few-public-methods
    def __init__(self, address):
        self._hid = hid.device()
        self._hid.open_path(address)
        print("Connected to " + str(address))
        self._gp_config = [0x07] * 4  # "don't care" initial value
        for pin in range(4):
            self.gp_set_mode(pin, self.GP_GPIO)  # set to GPIO mode
            self.gpio_set_direction(pin, 1)  # set to INPUT


class MCP2221I2C(_MCP2221I2C):  # pylint: disable=too-few-public-methods
    def __init__(self, mcp2221, *, frequency=100000):
        self._mcp2221 = mcp2221
        self._mcp2221.i2c_configure(frequency)


class I2C(busio.I2C):  # pylint: disable=too-few-public-methods
    def __init__(self, mcp2221_i2c):
        self._i2c = mcp2221_i2c


addresses = [mcp["path"] for mcp in hid.enumerate(0x04D8, 0x00DD)]

i2c_devices = []
i2c_devices.append(I2C(MCP2221I2C(_mcp2221)))

for addr in addresses:
    try:
        i2c_device = I2C(MCP2221I2C(MCP2221(addr)))
        i2c_devices.append(i2c_device)
    except OSError:
        print("Device path: " + str(addr) + " is used")


while True:
    for i2c in i2c_devices:
        addrbuf = bytearray(2)
        addrbuf[0] = ADDRID1 >> 8
        addrbuf[1] = ADDRID1 & 0xFF
        inbuf = bytearray(6)
        i2c.writeto_then_readfrom(MLXADDR, addrbuf, inbuf)
        print("Device " + str(i2c_devices.index(i2c)) + ": ")
        print(inbuf)
        time.sleep(0.5)
