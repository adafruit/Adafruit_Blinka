import sys
sys.path.append('/home/pi/Adafruit_Micropython_Blinka/src')
sys.path.append('/home/pi/Adafruit_Python_GPIO')

#from Adafruit_GPIO import Platform
#print("Platform = ", Platform.platform_detect(), Platform.pi_version())

from adafruit_blinka.agnostic import board as agnostic_board
print("hello blinka!")
print("Found system type: %s (sys.plaform %s implementation %s) " % (agnostic_board, sys.platform, sys.implementation.name))

import board

print(dir(board))

#print(adafruit_blinka.adafruit_blinka.agnostic.microcontroller)
