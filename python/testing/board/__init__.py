"""Configuration of testing fixtures depending on the board layout"""
import agnostic
import board
if agnostic.board == "feather_m0_express":
    default_pin = board.D5
    led_pin = board.D13
elif agnostic.board == "feather_huzzah":
    default_pin = board.GPIO4
    led_pin = board.GPIO2
