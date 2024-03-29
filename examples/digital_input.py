import time
import board
import digitalio

button = digitalio.DigitalInOut(board.G0)
button.direction = digitalio.Direction.INPUT

while True:
    print(f"Button value: {button.value}")
    time.sleep(0.5)