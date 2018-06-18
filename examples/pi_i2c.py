import sys
import time
sys.path.append('/home/pi/Adafruit_Micropython_Blinka/src')
sys.path.append('/home/pi/Adafruit_Python_GPIO')

import board
import digitalio
import busio

print("hello blinka!")


i2c = busio.I2C(board.SCL, board.SDA)

print([hex(i) for i in i2c.scan()])

led = digitalio.DigitalInOut(board.D4)
led.direction = digitalio.Direction.OUTPUT
led.value = True

