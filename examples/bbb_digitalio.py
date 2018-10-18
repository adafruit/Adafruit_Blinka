# Example of blinking LED on BeagleBone Black
# https://www.adafruit.com/product/1876
#
# Wire the circuit as follows:
# 1) connect anode (+) lead of LED to P9.12 pin
# 2) connect cathode (-) lead to 1K Ohm resistor
# 3) connect that 1K Ohm resistor to DGND (P9.1)

import time
import board
import digitalio

print("hello blinky!")

led = digitalio.DigitalInOut(board.P9_12)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
