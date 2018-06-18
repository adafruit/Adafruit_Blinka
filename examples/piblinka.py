import sys
import time
sys.path.append('/home/pi/Adafruit_Micropython_Blinka/src')
sys.path.append('/home/pi/Adafruit_Python_GPIO')

#from Adafruit_GPIO import Platform
#print("Platform = ", Platform.platform_detect(), Platform.pi_version())

print("hello blinka!")

from adafruit_blinka.agnostic import board as agnostic_board
print("Found system type: %s (sys.plaform %s implementation %s) " % (agnostic_board, sys.platform, sys.implementation.name))

import board
print("board contents: ", dir(board))

import digitalio

led = digitalio.DigitalInOut(board.D4)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.D18)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN

while True:
    led.value = button.value
    time.sleep(0.1)
    #led.value = False
    #time.sleep(0.5)
