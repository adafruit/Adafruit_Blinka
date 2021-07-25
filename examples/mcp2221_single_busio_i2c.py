import argparse
import busio


# Usage:
# $ lsusb | grep Microchip
# Bus 001 Device 082: ID 04d8:00dd Microchip Technology, Inc.
# Bus 001 Device 083: ID 04d8:00dd Microchip Technology, Inc.
# $ python mcp2221_single_busio_i2c.py -b 1 -d 83
# I2C devices found:  ['0x70']


# Bus and Device number can be gathered from `lsusb`
parser = argparse.ArgumentParser()
parser.add_argument(
    "-b", "--bus", type=int, required=True, help="USB bus number (base10)"
)
parser.add_argument(
    "-d", "--device", type=int, required=True, help="USB device number (base10)"
)
args = parser.parse_args()

# Need to be bytes, always function 2
device_path = "{:04x}:{:04x}:02".format(args.bus, args.device).encode()
i2c = busio.I2C(bus_id=device_path)
print("I2C devices found: ", [hex(i) for i in i2c.scan()])
