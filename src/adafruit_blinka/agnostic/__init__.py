"""Allows useful indirection to test Pin naming logic by switching platform in testing
    or provide bootstrapping logic for board identification where auto-detection is not
    feasible (e.g. multiple ESP8266 boards architecturally identical). Once runtime
    environment is established, can choose various routes to make available and re-export
    common modules and operations, depending on platform support
"""
import sys
import adafruit_platformdetect

# We intentionally are patching into this namespace as module names so skip the name check.
# pylint: disable=invalid-name

detect = adafruit_platformdetect.PlatformDetect()

board_name = detect.board.name()
chip_name = detect.chip.name()

implementation = sys.implementation.name
if implementation == "micropython":
    from utime import sleep
elif implementation == "circuitpython" or implementation == "cpython":
    from time import sleep
