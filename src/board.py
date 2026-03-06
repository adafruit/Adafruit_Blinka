# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`board` - Define ids for available pins
=================================================

See `CircuitPython:board` in CircuitPython for more details.

* Author(s): cefn, Melissa LeBlanc-Williams
"""

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_Blinka.git"
__blinka__ = True

import sys
import json
import adafruit_platformdetect.constants.boards as ap_board
from adafruit_blinka.agnostic import board_id, detector
from adafruit_blinka.importing import import_mod, get_import_file


# pylint: disable=wildcard-import,unused-wildcard-import,ungrouped-imports
# pylint: disable=import-outside-toplevel

SCL = SDA = SCLK = MOSI = MISO = None

# Start with micropython boards as importlib isn't available on those chips:

# Go through the board_list and import the first one that matches
# if the key start with any_ then use detector.board.any_...
with open(get_import_file("board_imports.json", __file__)) as f:
    board_imports = json.load(f)

    for board_key, board_module in board_imports.items():
        if board_key.startswith("any_"):
            if getattr(detector.board, board_key):
                import_mod(globals(), board_module)
                break
        else:
            if board_id == getattr(ap_board, board_key):
                import_mod(globals(), board_module)
                break
    else:
        if "sphinx" in sys.modules:
            pass

        elif board_id is None:
            import platform
            import pkg_resources

            package = str(
                pkg_resources.get_distribution("adafruit_platformdetect")
            ).split()
            raise NotImplementedError(
                f"""
                {package[0]} version {package[1]} was unable to identify the board and/or
                microcontroller running the {platform.system()} platform. Please be sure you
                have the latest packages by running:
                'pip3 install --upgrade adafruit-blinka adafruit-platformdetect'

                If you are running the latest package, your board may not yet be supported. Please
                open a New Issue on GitHub at https://github.com/adafruit/Adafruit_Blinka/issues and
                select New Board Request.
                """
            )
        else:
            raise NotImplementedError(f"Board not supported {board_id}.")

if SCL is not None and SDA is not None:

    def I2C():
        """The singleton I2C interface"""
        import busio

        return busio.I2C(SCL, SDA)


if SCLK is not None and MOSI is not None and MISO is not None:

    def SPI():
        """The singleton SPI interface"""
        import busio

        return busio.SPI(SCLK, MOSI, MISO)
