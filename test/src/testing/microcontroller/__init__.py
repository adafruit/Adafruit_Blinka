# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
from adafruit_blinka.agnostic import microcontroller

if microcontroller == "esp8266":
    pin_count = 10
elif microcontroller == "samd21":
    pin_count = 38
else:
    raise NotImplementedError("Microcontroller not supported")
