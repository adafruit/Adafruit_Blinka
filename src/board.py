# The MIT License (MIT)
#
# Copyright (c) 2017 cefn for adafruit industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`board` - Define ids for available pins
=================================================

See `CircuitPython:board` in CircuitPython for more details.

* Author(s): cefn
"""
import sys

from adafruit_blinka.agnostic import board_id, detector
import adafruit_platformdetect.board as ap_board

# pylint: disable=wildcard-import,unused-wildcard-import,ungrouped-imports

if board_id == ap_board.FEATHER_HUZZAH:
    from adafruit_blinka.board.feather_huzzah import *

elif board_id == ap_board.NODEMCU:
    from adafruit_blinka.board.nodemcu import *

elif board_id == ap_board.PYBOARD:
    from adafruit_blinka.board.pyboard import *

elif detector.board.any_raspberry_pi_40_pin:
    from adafruit_blinka.board.raspi_40pin import *

elif detector.board.RASPBERRY_PI_B_REV1:
    from adafruit_blinka.board.raspi_1b_rev1 import *

elif detector.board.RASPBERRY_PI_B_REV2:
    from adafruit_blinka.board.raspi_1b_rev2 import *

elif board_id == ap_board.BEAGLEBONE_BLACK:
    from adafruit_blinka.board.beaglebone_black import *

elif board_id == ap_board.BEAGLEBONE_POCKETBEAGLE:
    from adafruit_blinka.board.beaglebone_pocketbeagle import *

elif board_id == ap_board.ORANGE_PI_PC:
    from adafruit_blinka.board.orangepipc import *

elif board_id == ap_board.GIANT_BOARD:
    from adafruit_blinka.board.giantboard import *

elif board_id == ap_board.JETSON_TX1:
    from adafruit_blinka.board.jetson_tx1 import *

elif board_id == ap_board.JETSON_TX2:
    from adafruit_blinka.board.jetson_tx2 import *

elif board_id == ap_board.JETSON_XAVIER:
    from adafruit_blinka.board.jetson_xavier import *

elif board_id == ap_board.JETSON_NANO:
    from adafruit_blinka.board.jetson_nano import *

elif board_id == ap_board.CORAL_EDGE_TPU_DEV:
    from adafruit_blinka.board.coral_edge_tpu import *

elif "sphinx" in sys.modules:
    pass

else:
    raise NotImplementedError("Board not supported")

def I2C():
    """The singleton I2C interface"""
    import busio
    return busio.I2C(SCL, SDA)

def SPI():
    """The singleton SPI interface"""
    import busio
    return busio.SPI(SCLK, MOSI, MISO)
