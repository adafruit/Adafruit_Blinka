import os
from adafruit_blinka.microcontroller.rp2040_u2if.pin import Pin
from adafruit_blinka.microcontroller.rp2040_u2if.rp2040_u2if import RP2040_u2if
from specific_board import init_specific_board, display_connected_rp2040, RP2040_u2if_init

os.environ["BLINKA_U2IF"]="1"


display_connected_rp2040()


import time
import adafruit_apds9960.apds9960
# Initialize I2C using u2if's I2C interface
#board2=init_specific_board(0xE6636825930C7C23)

#This class is more low level, used mostly for GPIO manipulation.
rp = RP2040_u2if_init("0xE6636825930C7C23")


# This is high level adafruit class used for I2C.
# Do not import the board class if you are using multiple rp2040  without this method as you cant control the serial of the board
board1, busio1=init_specific_board("0xE462B0659F1B2036")
i2c = busio1.I2C(board1.GP5, board1.GP4)  # SCL, SDA for default I2C1
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)


# Enable color sensing
sensor.enable_color = True

print("INIT GPIO")
rp.gpio_init_pin(0, Pin.OUT,Pin.PULL_NONE)
rp.gpio_init_pin(1, Pin.IN,Pin.PULL_NONE)
# Main loop to read RGB data
print("Inside main loop")
r, g, b, c = 1,1,1,1
while True:
    r, g, b, c = sensor.color_data  # Red, Green, Blue, and Clear channel data
    print(f"Red: {r}, Green: {g}, Blue: {b}, Clear: {c}")
    if r > g and r > b:
        print("RED")
    if g > r and g > b:
        print("GREEN")
    if b > g and b > r:
        print("BLUE")
    print(rp.gpio_get_pin(1))
    (rp.gpio_set_pin(0, 0))
    time.sleep(2)
    (rp.gpio_set_pin(0, 1))
    time.sleep(1)
