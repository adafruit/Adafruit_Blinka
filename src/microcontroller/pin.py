"""Pins named after their chip name."""

from adafruit_blinka import agnostic

# We intentionally are patching into this namespace so skip the wildcard check.
# pylint: disable=unused-wildcard-import,wildcard-import

if agnostic.platform == "esp8266":
    from adafruit_blinka.microcontroller.esp8266.pin import *
elif agnostic.platform == "stm32":
    from adafruit_blinka.microcontroller.stm32.pin import *
elif agnostic.platform == "linux":
    if agnostic.board_id == "raspi_3" or agnostic.board_id == "raspi_2":
        from adafruit_blinka.microcontroller.raspi_23.pin import *
    else:
        raise NotImplementedError("Board not supported: ", agnostic.board_id)
else:
    raise NotImplementedError("Microcontroller not supported")
