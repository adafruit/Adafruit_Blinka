import agnostic
from mcp import Enum

class Pin(Enum):
    def __init__(self, id):
        """Identifier for pin, referencing platform-specific pin id"""
        self.id = id
    pass

if agnostic.microcontroller == "esp8266":
    from microcontroller.esp8266 import pin
elif agnostic.microcontroller == "stm32":
    from microcontroller.stm32 import pin
