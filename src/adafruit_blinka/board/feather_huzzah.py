# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Feather Huzzah."""

from adafruit_blinka.microcontroller.esp8266 import pin

# TODO need equiv of INPUT_PULL_DOWN_16 ?
# See https://tttapa.github.io/ESP8266/Chap04%20-%20Microcontroller.html

GPIO0 = pin.GPIO0
GPIO1 = pin.GPIO1
GPIO2 = pin.GPIO2
GPIO3 = pin.GPIO3
GPIO4 = pin.GPIO4
GPIO5 = pin.GPIO5
GPIO12 = pin.GPIO12
GPIO13 = pin.GPIO13
GPIO14 = pin.GPIO14
GPIO15 = pin.GPIO15
GPIO16 = pin.GPIO16

ADC = pin.TOUT

MISO = GPIO12
MOSI = GPIO13
SCK = GPIO14

RX = GPIO3
TX = GPIO1

SDA = GPIO4
SCL = GPIO5
