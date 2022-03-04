# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Configuration of testing fixtures depending on the board layout"""
from adafruit_blinka import agnostic

import board

if agnostic.board == "feather_m0_express":
    default_pin = board.D5
    led_pin = board.D13
    led_hardwired = True
    led_inverted = False
elif agnostic.board == "feather_huzzah":
    default_pin = board.GPIO4
    led_pin = board.GPIO0  # red led
    led_hardwired = True
    led_inverted = True
elif agnostic.board == "pyboard":
    default_pin = board.X1
    led_pin = board.LED_BLUE
    led_hardwired = True
    led_inverted = False
    uartTxId = "B6"
    uartRXId = "B7"
else:
    raise NotImplementedError("Board not supported")
