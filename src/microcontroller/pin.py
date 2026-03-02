# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pins named after their chip name."""
import sys
import json
from adafruit_platformdetect.constants import chips as ap_chip
from adafruit_blinka.agnostic import chip_id, detector
from adafruit_blinka.importing import import_mod, get_import_file

# We intentionally are patching into this namespace so skip the wildcard check.
# pylint: disable=unused-wildcard-import,wildcard-import,ungrouped-imports

with open(get_import_file("microcontroller_imports.json", __file__)) as f:
    microcontroller_imports = json.load(f)

    for chip_key, chip_module in microcontroller_imports.items():
        if getattr(detector.board, chip_key) and isinstance(chip_module, dict):
            # Loop through the children and import the first one that matches
            for board_key, board_module in chip_module.items():
                if board_key.startswith("any_") and getattr(detector.board, board_key):
                    # import Pin from the microcontroller module
                    import_mod(f"{board_module}.pin", "*")
                    break
                if board_key == getattr(detector.board, board_key):
                    import_mod(f"{board_module}.pin", "*")
                    break
            else:
                import_mod(f"{chip_module['default']}.pin", "*")
        else:
            if chip_key.startswith("board.") and getattr(detector.board, chip_key[6:]):
                # Case 2
                import_mod(f"{chip_module}.pin", "*")
                break
            if getattr(detector.chip, chip_key):
                import_mod(f"{chip_module}.pin", "*")
                break
    else:
        if "sphinx" in sys.modules:
            # pylint: disable=unused-import
            from adafruit_blinka.microcontroller.generic_micropython import Pin
        elif chip_id == ap_chip.GENERIC_X86:
            print("WARNING: GENERIC_X86 is not fully supported. Some features may not work.")
            from adafruit_blinka.microcontroller.generic_micropython import Pin
        elif chip_id is None:
            print(
                "WARNING: chip_id == None is not fully supported. Some features may not work."
            )
            from adafruit_blinka.microcontroller.generic_micropython import Pin
        else:
            raise NotImplementedError("Microcontroller not supported: ", chip_id)
