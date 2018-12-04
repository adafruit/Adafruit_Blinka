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

from adafruit_blinka.agnostic import board_id

if board_id == "feather_huzzah":
    from adafruit_blinka.board.feather_huzzah import *
elif board_id == "nodemcu":
    from adafruit_blinka.board.nodemcu import *
elif board_id == "pyboard":
    from adafruit_blinka.board.pyboard import *
elif board_id == "raspi_2" or board_id == "raspi_3":
    from adafruit_blinka.board.raspi_23 import *
elif board_id == "beaglebone_black":
    from adafruit_blinka.board.beaglebone_black import *
elif board_id == "orangepipc":
    from adafruit_blinka.board.orangepipc import *
elif board_id == "giantboard":
    from adafruit_blinka.board.giantboard import *
elif "sphinx" in sys.modules:
    pass
else:
    raise NotImplementedError("Board not supported")
