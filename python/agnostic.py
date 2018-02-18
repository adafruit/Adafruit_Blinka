"""Allows useful indirection to test Pin naming logic by switching platform in testing
    or provide bootstrapping logic for board identification where auto-detection is not
    feasible (e.g. multiple ESP8266 boards architecturally identical). Once runtime
    environment is established, can choose various routes to make available and re-export
    common modules and operations, depending on platform support
"""
import sys

try:
    microcontroller = sys.platform
except:
    microcontroller = None

# TODO switch name of platform below to be microcontroller
if microcontroller is not None:
    if microcontroller == "esp8266":
        board = "feather_huzzah"
    elif microcontroller == "samd21":
        board="feather_m0_express"
    elif microcontroller == "pyboard":
        microcontroller= "stm32"
        board="pyboard"
else:
    board = None

implementation = sys.implementation.name
if implementation == "micropython":
    import utime as time
elif implementation == "circuitpython":
    import time