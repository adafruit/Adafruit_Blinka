"""Pins named after their chip name."""

import adafruit_platformdetect.chip as ap_chip
from adafruit_blinka.agnostic import chip_id

# We intentionally are patching into this namespace so skip the wildcard check.
# pylint: disable=unused-wildcard-import,wildcard-import,ungrouped-imports

if chip_id == ap_chip.ESP8266:
    from adafruit_blinka.microcontroller.esp8266.pin import *
elif chip_id == ap_chip.STM32:
    from adafruit_blinka.microcontroller.stm32.pin import *
elif chip_id == ap_chip.BCM2XXX:
    from adafruit_blinka.microcontroller.bcm283x.pin import *
elif chip_id == ap_chip.AM33XX:
    from adafruit_blinka.microcontroller.am335x.pin import *
elif chip_id == ap_chip.SUN8I:
    from adafruit_blinka.microcontroller.allwinner_h3.pin import *
elif chip_id == ap_chip.SAMA5:
    from adafruit_blinka.microcontroller.sama5.pin import *
elif chip_id == ap_chip.T210:
    from adafruit_blinka.microcontroller.tegra.t210.pin import *
elif chip_id == ap_chip.T186:
    from adafruit_blinka.microcontroller.tegra.t186.pin import *
elif chip_id == ap_chip.T194:
    from adafruit_blinka.microcontroller.tegra.t194.pin import *
elif chip_id == ap_chip.IMX8MX:
    from adafruit_blinka.microcontroller.nxp_imx8m.pin import *
else:
    raise NotImplementedError("Microcontroller not supported: ", chip_id)
