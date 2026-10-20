# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""MCP2221-specific activity indicators; run with BLINKA_MCP2221=1.

For each LED, connect the logic supply (3V on the default Adafruit breakout)
through a 1 kohm resistor to the LED anode, and its cathode to G0, G1, or G3.
The indicators are active-low and pulse automatically during their bus traffic.
These modes are not alternate I2C/UART data pins, and are not digitalio modes.
UART indicators require traffic on the separate USB serial port.

Settings are volatile until reset. No flash configuration is written. This
example restores the three pins to GPIO inputs on exit while the USB session
is healthy. After a USB transport error, reconnect the device and restart the
program; cleanup cannot guarantee the physical pin state. Normal GPIO/ADC/DAC
configuration of a pin also replaces that pin's activity-indicator mode.
"""

import time

import board
from adafruit_blinka.microcontroller.mcp2221.pin import Pin

i2c = None
try:
    board.G0.init(mode=Pin.LED_URX)
    board.G1.init(mode=Pin.LED_UTX)
    board.G3.init(mode=Pin.LED_I2C)
    i2c = board.I2C()

    while True:
        if i2c.try_lock():
            try:
                print("I2C addresses:", [hex(address) for address in i2c.scan()])
            finally:
                i2c.unlock()
        time.sleep(1)
finally:
    for pin in (board.G0, board.G1, board.G3):
        pin.init(mode=Pin.IN)
    if i2c is not None:
        i2c.deinit()
