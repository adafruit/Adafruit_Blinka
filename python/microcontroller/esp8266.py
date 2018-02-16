from mcp import Enum
class Pin(Enum):
    def __init__(self, num):
        self.num = num
    pass
Pin.GPIO0=Pin(0)
Pin.GPIO2=Pin(2)
Pin.GPIO4=Pin(4)
Pin.GPIO5=Pin(5)
Pin.GPIO12=Pin(12)
Pin.GPIO13=Pin(13)
Pin.GPIO14=Pin(14)
Pin.GPIO15=Pin(15)
Pin.GPIO16=Pin(16)


class cpu():
    def frequency(self):
        from machine import freq
        return freq()
