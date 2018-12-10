"""Pins named after their chip name."""

from adafruit_blinka import agnostic
import adafruit_platformdetect.chip as ap_chip

# We intentionally are patching into this namespace so skip the wildcard check.
# pylint: disable=unused-wildcard-import,wildcard-import
if agnostic.chip_name == ap_chip.ESP8266:
    from adafruit_blinka.microcontroller.esp8266.pin import *
elif agnostic.chip_name == ap_chip.STM32:
    from adafruit_blinka.microcontroller.stm32.pin import *
elif agnostic.detect.any_raspberry_pi_or_3:
    from adafruit_blinka.microcontroller.raspi_23.pin import *
elif agnostic.detect.beaglebone_black:
    from adafruit_blinka.microcontroller.beaglebone_black.pin import *
elif agnostic.detect.orangepi_pc:
    from adafruit_blinka.microcontroller.allwinner_h3.pin import *
else:
    raise NotImplementedError("Board / microcontroller not supported: ", agnostic.board_name)
