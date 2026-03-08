# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`microcontroller` - Pin references and cpu functionality
========================================================

* Author(s): Melissa LeBlanc-Williams
"""
import sys
import json
import time

from adafruit_platformdetect.constants import chips as ap_chip
from adafruit_blinka.agnostic import chip_id, detector
from adafruit_blinka.importing import import_mod, get_import_file
from microcontroller import pin  # pylint: disable=unused-import
from microcontroller.pin import Pin  # pylint: disable=unused-import


def delay_us(delay):
    """Sleep for delay usecs."""
    time.sleep(delay / 1e6)


# We intentionally are patching into this namespace so skip the wildcard check.
# pylint: disable=unused-wildcard-import,wildcard-import,ungrouped-imports

with open(get_import_file("../microcontroller_imports.json", __file__)) as f:
    microcontroller_imports = json.load(f)

    for chip_key, chip_module in microcontroller_imports.items():
        if getattr(detector.chip, chip_key):
            if isinstance(chip_module, dict):
                # Loop through the children and import the first one that matches
                for board_key, board_chip_module in chip_module.items():
                    if board_key.startswith("any_") and getattr(
                        detector.board, board_key
                    ):
                        # import Pin from the microcontroller module
                        import_mod(globals(), f"{board_chip_module}.pin", "*")
                        break
                    if board_key == getattr(detector.board, board_key):
                        import_mod(globals(), f"{board_chip_module}.pin", "*")
                        break
                else:
                    import_mod(globals(), f"{chip_module['default']}.pin", "*")
                break
            import_mod(globals(), f"{chip_module}.pin", "*")
            break
    else:
        if chip_id == ap_chip.GENERIC_X86:
            print(
                "WARNING: GENERIC_X86 is not fully supported. Some features may not work."
            )
        elif chip_id is None:
            print(
                "WARNING: chip_id == None is not fully supported. Some features may not work."
            )
        elif "sphinx" in sys.modules:
            pass
        else:
            raise NotImplementedError("Microcontroller not supported: ", chip_id)
