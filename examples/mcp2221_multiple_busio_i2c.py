import busio
import hid


# Usage:
# $ python mcp2221_multiple_busio_i2c.py
# I2C devices found:  []
# I2C devices found:  ['0x70']


MCP2221_VID = 0x04D8
MCP2221_PID = 0x00DD

i2c_busses = []
addresses = [mcp["path"] for mcp in hid.enumerate(MCP2221_VID, MCP2221_PID)]

for address in addresses:
    i2c_busses.append(busio.I2C(bus_id=address))

for i2c in i2c_busses:
    print("I2C devices found: ", [hex(i) for i in i2c.scan()])
