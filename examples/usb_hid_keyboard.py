# SPDX-FileCopyrightText: 2023 Björn Bösel for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
USB HID Keyboard Example for Raspberry Pi Zero (W)
===================================================

Demonstrates how to use Blinka's ``usb_hid`` module to turn a
Raspberry Pi Zero into a USB HID keyboard.

Prerequisites
-------------
1. Enable the dwc2 overlay (once, then reboot)::

       sudo bash -c "echo 'dtoverlay=dwc2' >> /boot/config.txt"
       sudo reboot

2. Load the libcomposite kernel module::

       sudo modprobe libcomposite

   To make it persistent across reboots::

       sudo bash -c "echo 'libcomposite' >> /etc/modules"

3. Install the CircuitPython HID library::

       pip3 install adafruit-circuitpython-hid

Wiring
------
- Wire a button between GP20 and GND (types Shift+A).
- Wire a button between GP21 and GND (types "Hello World!").
- Wire an LED + 1k resistor between GP16 and GND.
- Connect the Pi Zero to the host computer via USB.

Run with::

    sudo -E python3 usb_hid_keyboard.py

The ``-E`` flag preserves the user environment so pip-installed
packages are found when running as root.
"""

import time

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

import board
import digitalio
import usb_hid
from usb_hid import Device

# Button pins (activate internal pull-ups)
keypress_pins = [board.D20, board.D21]

# What each button sends: a Keycode or a string
keys_pressed = [Keycode.A, "Hello World!\n"]
control_key = Keycode.SHIFT

# Set up button inputs with pull-ups
key_pin_array = []
for pin in keypress_pins:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pin_array.append(key_pin)

# Set up LED output
led = digitalio.DigitalInOut(board.D16)
led.direction = digitalio.Direction.OUTPUT

# Create the USB HID keyboard
usb_hid.enable([Device.KEYBOARD], boot_device=0)
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

print("Waiting for key press...")

while True:
    for key_pin in key_pin_array:
        if not key_pin.value:  # Button pressed (grounded)
            i = key_pin_array.index(key_pin)
            print("Pin #%d is grounded." % i)

            led.value = True

            while not key_pin.value:
                pass  # Wait for release

            key = keys_pressed[i]
            if isinstance(key, str):
                keyboard_layout.write(key)
            else:
                keyboard.press(control_key, key)
                keyboard.release_all()

            led.value = False

    time.sleep(0.01)
