import sys
import time
sys.path.append('/home/pi/Adafruit_Micropython_Blinka/src')
sys.path.append('/home/pi/Adafruit_Python_GPIO')
sys.path.append('/home/pi/Adafruit_Python_PureIO')

import board
import digitalio
import busio

spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
while not spi.try_lock():
    pass
spi.configure(baudrate=16000000)
spi.unlock()

while True:
    spi.write(bytes([x for x in range(64)]))
    time.sleep(0.1)
