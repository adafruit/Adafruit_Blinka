from adafruit_blinka import Enum, agnostic


class Pin(Enum):
    def __init__(self, id):
        """Identifier for pin, referencing platform-specific pin id"""
        self.id = id

    def __repr__(self):
        import board
        for key in dir(board):
            if getattr(board, key) is self:
                return "board.{}".format(key)
        import microcontroller
        for key in dir(microcontroller):
            if getattr(microcontroller, key) is self:
                return "microcontroller.{}".format(key)
        return repr(self)


if agnostic.microcontroller == "esp8266":
    from adafruit_blinka.microcontroller.esp8266 import *
elif agnostic.microcontroller == "stm32":
    from adafruit_blinka.microcontroller.stm32 import *
else:
    raise NotImplementedError("Microcontroller not supported")