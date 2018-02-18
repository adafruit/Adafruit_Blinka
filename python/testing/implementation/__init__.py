import agnostic
import board
if agnostic.board == "feather_m0_express":
    default_pin = board.D5
    led_pin = board.D13
    pin_count = 38
elif agnostic.board == "feather_huzzah":
    default_pin = board.D5
    led_pin = board.D2
    pin_count = 10
