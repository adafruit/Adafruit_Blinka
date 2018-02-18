"""Allows useful indirection to test Pin naming logic by switching platform in testing
    or where auto-detection is not feasible (e.g. multiple ESP8266 boards architecturally identical)
"""
import sys

try:
    platform = sys.platform
except:
    platform = None

if platform is not None:
    if platform == "esp8266":
        board = "huzzah"
    elif platform == "Atmel SAMD21":
        board="feather_m0_express"
    elif platform == "pyboard":
        platform="STM32F405RG"
        board="pyboard"
else:
    board = None

implementation = sys.implementation.name
if implementation == "micropython":
    import utime as time
elif implementation == "circuitpython":
    import time