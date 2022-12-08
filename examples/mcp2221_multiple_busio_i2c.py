# SPDX-FileCopyrightText: 2022, The Blinka Authors.
#
# SPDX-License-Identifier: MIT

import busio

from adafruit_blinka.microcontroller.mcp2221.mcp2221 import MCP2221

# Usage:
# $ python mcp2221_multiple_busio_i2c.py
# 2 MCP2221 found: [b'2-3.3:1.2', b'2-3.2:1.2']
# I2C devices found on 2-3.3:1.2: ['0x77']
# I2C devices found on 2-3.2:1.2: ['0x58', '0x61']

# # MCP2221.available_paths() is roughly equivalent to
# import hid
# MCP2221_VID = 0x04D8
# MCP2221_PID = 0x00DD
# addresses = [mcp["path"] for mcp in hid.enumerate(MCP2221_VID, MCP2221_PID)]

addresses = MCP2221.available_paths()
print(f"{len(addresses)} MCP2221(s) found: {addresses}")

i2c_busses = []
for address in addresses:
    i2c_busses.append(busio.I2C(bus_id=address))

for address, i2c in zip(addresses, i2c_busses):
    print(f"I2C devices found on {address.decode()}:", [hex(i) for i in i2c.scan()])
