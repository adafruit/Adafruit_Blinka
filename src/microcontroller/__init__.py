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
        import microcontroller.pin as pin
        for key in dir(pin):
            if getattr(pin, key) is self:
                return "microcontroller.pin.{}".format(key)
        return repr(self)


if agnostic.microcontroller == "esp8266":
    from adafruit_blinka.microcontroller.esp8266 import *
elif agnostic.microcontroller == "stm32":
    from adafruit_blinka.microcontroller.stm32 import *
else:
    raise NotImplementedError("Microcontroller not supported")