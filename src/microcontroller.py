from adafruit_blinka import Enum, agnostic


class Pin(Enum):
    def __init__(self, id):
        """Identifier for pin, referencing platform-specific pin id"""
        self.id = id
    pass

if agnostic.microcontroller == "esp8266":
    pass
elif agnostic.microcontroller == "stm32":
    pass
else:
    raise NotImplementedError("Microcontroller not supported")