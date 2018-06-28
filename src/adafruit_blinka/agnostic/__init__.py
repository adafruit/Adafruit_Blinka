"""Allows useful indirection to test Pin naming logic by switching platform in testing
    or provide bootstrapping logic for board identification where auto-detection is not
    feasible (e.g. multiple ESP8266 boards architecturally identical). Once runtime
    environment is established, can choose various routes to make available and re-export
    common modules and operations, depending on platform support
"""
import sys

# We intentionally are patching into this namespace as module names so skip the name check.
# pylint: disable=invalid-name
microcontroller = sys.platform

board = None
if microcontroller is not None:
    if microcontroller == "esp8266":  # TODO more conservative board-guessing
        board = "feather_huzzah"
    elif microcontroller == "samd21":
        board = "feather_m0_express"
    elif microcontroller == "pyboard":
        microcontroller = "stm32"
        board = "pyboard"
    elif microcontroller == "linux":
        from Adafruit_GPIO import Platform
        if Platform.platform_detect() == Platform.RASPBERRY_PI:
            if Platform.pi_version() == 1:
                board = "raspi_1"
            elif Platform.pi_version() == 2:
                board = "raspi_2"
            elif Platform.pi_version() == 3:
                board = "raspi_3"

implementation = sys.implementation.name
if implementation == "micropython":
    from utime import sleep
elif implementation == "circuitpython" or implementation == "cpython":
    from time import sleep
