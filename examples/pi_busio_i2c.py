import time
import sys
import board
import busio

print("hello blinka!")

i2c = busio.I2C(board.SCL, board.SDA)

print("I2C devices found: ", [hex(i) for i in i2c.scan()])

if not 0x18 in i2c.scan():
    print("Didn't find MCP9808")
    sys.exit()


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
