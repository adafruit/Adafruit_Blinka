import busio


# Usage:
# $ python mcp2221_first_busio_i2c.py
# I2C devices found:  ['0x70']


i2c = busio.I2C()
print("I2C devices found: ", [hex(i) for i in i2c.scan()])
