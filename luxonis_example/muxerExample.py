import os
os.environ["BLINKA_U2IF"]="1"
from time import sleep
from specific_board import init_specific_board, display_connected_rp2040, RP2040_u2if_init
import digitalio
display_connected_rp2040()



# led 0 means the USB is on the LED soldiered side

# Set up a GPIO pin as an output
board, busio = init_specific_board("0xE6636825930C7C23")

button = digitalio.DigitalInOut(board.GP0)
button.direction = digitalio.Direction.OUTPUT
button.value=True

usbLed = digitalio.DigitalInOut(board.GP1)
usbLed.direction = digitalio.Direction.INPUT

def press_button(button):
    print("Pressing button")
    button.value = False
    # If delay is too small button will not siwtch. With delay of 3 seconds, this worked pretty much 100% od the time
    sleep(3)
    button.value = True
    #If you retry multiple times, you need this delay.
    sleep(2)


def toogle_to_correct(led, button, wanted_state):
    for i in range(5):
        if bool(int(wanted_state)) == led.value:
            return True
        else:
            press_button(button)

    raise Exception("Toogle unsuccessful, didnt change states")


while True:
    toogle_to_correct(usbLed, button, True)
    print(usbLed.value)
    sleep(1)
    toogle_to_correct(usbLed, button, False)
    print(usbLed.value)
