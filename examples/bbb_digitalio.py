#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Example of blinking LED on BeagleBone Black
# https://www.adafruit.com/product/1876
#
# Wire the circuit as follows:
# 1) connect anode (+) lead of LED to P9.12 pin
# 2) connect cathode (-) lead to 1K Ohm resistor
# 3) connect that 1K Ohm resistor to DGND (P9.1)
#
# NOTE: the pin mode can be verified with the command line
# utility config-pin on the BeagleBoard.org Debian image
#
# To verify the pin is in GPIO mode:
# debian@beaglebone:~$ config-pin -q p9.12
# P9_12 Mode: gpio Direction: out Value: 0
#
# To set pin to GPIO mode:
# $ config-pin p9.12 gpio

import time
import board
import digitalio

print("hello blinky!")

led = digitalio.DigitalInOut(board.P9_12)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
