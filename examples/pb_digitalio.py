#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Example of blinking LED on PocketBeagle
# https://www.adafruit.com/product/4179
#
# Wire the circuit as follows:
# 1) connect anode (+) lead of LED to P1_33 pin
# 2) connect cathode (-) lead to 1K Ohm resistor
# 3) connect that 1K Ohm resistor to GND
#
# NOTE: the pin mode can be verified with the command line
# utility config-pin on the BeagleBoard.org Debian image
#
# To verify the pin is in GPIO mode:
# debian@beaglebone:~$ config-pin -q p1.33
# P1_33 Mode: gpio Direction: out Value: 0
#
# To set pin to GPIO mode:
# $ config-pin p1.33 gpio

import time
import board
import digitalio

print("hello blinky!")

led = digitalio.DigitalInOut(board.P1_33)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
