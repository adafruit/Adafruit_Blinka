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

# We'll define board and chip id values in agnostic rather than accessing
# detector directly elsewhere, just in case additional indirection is necessary
# at some later point:

detector = adafruit_platformdetect.Detector()
chip_id = detector.chip.id
board_id = detector.board.id

implementation = sys.implementation.name
if implementation == "micropython":
    from utime import sleep
elif implementation in ("circuitpython", "cpython"):
    from time import sleep
