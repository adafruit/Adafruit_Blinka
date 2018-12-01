"""Allows useful indirection to test Pin naming logic by switching platform in testing
    or provide bootstrapping logic for board identification where auto-detection is not
    feasible (e.g. multiple ESP8266 boards architecturally identical). Once runtime
    environment is established, can choose various routes to make available and re-export
    common modules and operations, depending on platform support
"""
import sys

# We intentionally are patching into this namespace as module names so skip the name check.
# pylint: disable=invalid-name
platform = sys.platform

board_id = None

if platform is not None:
    if platform == "esp8266":  # TODO more conservative board-guessing
        board_id = "feather_huzzah"
    elif platform == "samd21":
        board_id = "feather_m0_express"
    elif platform == "pyboard":
        platform = "stm32"
        board_id = "pyboard"
    elif platform == "linux":
        import re
        # we're going to redo the Platform detection, this is a terrible hack
        # for now.
        try:
            # lets see if we're an armbian board
            for line in open("/etc/armbian-release", 'r'):
                #print(line)
                m = re.search('BOARD=(.*)', line)
                if m:
                    board_id = m.group(1)
        except:
            from Adafruit_GPIO import Platform
            if Platform.platform_detect() == Platform.RASPBERRY_PI:
                if Platform.pi_version() == 1:
                    board_id = "raspi_1"
                elif Platform.pi_version() == 2:
                    board_id = "raspi_2"
                elif Platform.pi_version() == 3:
                    board_id = "raspi_3"
            elif Platform.platform_detect() == Platform.BEAGLEBONE_BLACK:
                board_id = "beaglebone_black"

implementation = sys.implementation.name
if implementation == "micropython":
    from utime import sleep
elif implementation == "circuitpython" or implementation == "cpython":
    from time import sleep
