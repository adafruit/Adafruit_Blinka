"""Configuration of testing fixtures depending on the board layout"""
from adafruit_blinka import agnostic

if agnostic.board == "feather_m0_express":
    default_pin = feather_m0_express.D5
    led_pin = feather_m0_express.D13
    led_hardwired = True
    led_inverted = False
elif agnostic.board == "feather_huzzah":
    from adafruit_blinka.board import feather_huzzah

    default_pin = feather_huzzah.GPIO4
    led_pin = feather_huzzah.GPIO0 # red led
    led_hardwired = True
    led_inverted = True
elif agnostic.board == "pyboard":
    default_pin = pyboard.X1
    led_pin = adafruit_blinka.board.pyboard.LED_BLUE
    led_hardwired = True
    led_inverted = False
else:
    raise NotImplementedError("Board not supported")
