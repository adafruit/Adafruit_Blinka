import sys
import time
import adafruit_blinka.agnostic as agnostic
import board
import digitalio

# from Adafruit_GPIO import Platform
# print("Platform = ", Platform.platform_detect(), Platform.pi_version())

print("hello blinka!")

print(
    "Found system type: %s (sys.platform %s implementation %s) "
    % (agnostic.board_id, sys.platform, sys.implementation.name)
)

print("board contents: ", dir(board))


led = digitalio.DigitalInOut(board.D4)
led.direction = digitalio.Direction.OUTPUT

button = digitalio.DigitalInOut(board.D18)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN

while True:
    led.value = button.value
    time.sleep(0.1)
