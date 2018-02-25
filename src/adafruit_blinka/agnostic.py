"""Allows useful indirection to test Pin naming logic by switching platform in testing
    or provide bootstrapping logic for board identification where auto-detection is not
    feasible (e.g. multiple ESP8266 boards architecturally identical). Once runtime
    environment is established, can choose various routes to make available and re-export
    common modules and operations, depending on platform support
"""
import gc
import sys
gc.collect()

try:
    microcontroller = sys.platform
except:
    microcontroller = None

board = None
if microcontroller is not None:
    if microcontroller == "esp8266":  # TODO more conservative board-guessing
        board = "feather_huzzah"
    elif microcontroller == "samd21":
        board = "feather_m0_express"
    elif microcontroller == "pyboard":
        microcontroller = "stm32"
        board = "pyboard"

implementation = sys.implementation.name
if implementation == "micropython":
    from utime import sleep
elif implementation == "circuitpython":
    from time import sleep
gc.collect()
