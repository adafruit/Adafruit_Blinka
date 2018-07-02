"""Microcontroller pins"""

from adafruit_blinka import Enum
from adafruit_blinka.agnostic import board_id, platform

class Pin(Enum):
    """Reference Pin object"""
    def __init__(self, pin_id):
        """Identifier for pin, referencing platform-specific pin id"""
        self._id = pin_id

    def __repr__(self):
        import board
        for key in dir(board):
            if getattr(board, key) is self:
                return "board.{}".format(key)
        import microcontroller.pin as pin
        for key in dir(pin):
            if getattr(pin, key) is self:
                return "microcontroller.pin.{}".format(key)
        return repr(self)

# We intentionally are patching into this namespace so skip the wildcard check.
# pylint: disable=unused-wildcard-import,wildcard-import

if platform == "esp8266":
    from adafruit_blinka.microcontroller.esp8266 import *
elif platform == "stm32":
    from adafruit_blinka.microcontroller.stm32 import *
elif platform == "linux":
    if board_id == "raspi_3" or board_id == "raspi_2":
        from adafruit_blinka.microcontroller.raspi_23 import *
    else:
        raise NotImplementedError("Board not supported:", board_id)
else:
    raise NotImplementedError("Platform not supported:", platform)
