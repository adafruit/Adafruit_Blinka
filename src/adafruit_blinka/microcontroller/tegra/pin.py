import sys
import Jetson.GPIO as GPIO
sys.path.append("/opt/nvidia/jetson-gpio/lib/python")
sys.path.append("/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO")
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)   # shh!

# Each Jetson model uses different I2C busses
JETSON_I2C_BUS_DEFS = {
    "JETSON_TX1": [0, 1],
    "JETSON_TX2": [1, 0],
    "JETSON_XAVIER": [8, 1],
    "JETSON_NANO": [1, 0]
}

model = GPIO.get_model()
I2C_BUS = JETSON_I2C_BUS_DEFS[model][0]
I2C_BUS_1 = JETSON_I2C_BUS_DEFS[model][1]

# Pins dont exist in CPython so...lets make our own!
class Pin:
    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2

    id = None
    _value = LOW
    _mode = IN

    def __init__(self, bcm_number):
        self.id = bcm_number

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        if mode != None:
            if mode == self.IN:
                self._mode = self.IN
                GPIO.setup(self.id, GPIO.IN)
            elif mode == self.OUT:
                self._mode = self.OUT
                GPIO.setup(self.id, GPIO.OUT)
            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)
        if pull != None:
            if self._mode != self.IN:
                raise RuntimeError("Cannot set pull resistor on output")
            if pull == self.PULL_UP:
                GPIO.setup(self.id, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            elif pull == self.PULL_DOWN:
                GPIO.setup(self.id, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            else:
                raise RuntimeError("Invalid pull for pin: %s" % self.id)

    def value(self, val=None):
        if val != None:
            if val == self.LOW:
                self._value = val
                GPIO.output(self.id, val)
            elif val == self.HIGH:
                self._value = val
                GPIO.output(self.id, val)
            else:
                raise RuntimeError("Invalid value for pin")
        else:
            return GPIO.input(self.id)

    def cleanup(self, channel=None):
        if channel is None:
            GPIO.cleanup()
        elif channel == self:
            GPIO.cleanup(self.id)
        else:
            raise RuntimeError("Invalid pin to cleanup")

D1 = Pin(1)
D2 = Pin(2)
D3 = Pin(3)
SDA = Pin(3)
D4 = Pin(4)
D5 = Pin(5)
SCL = Pin(5)
D6 = Pin(6)
D7 = Pin(7)
D8 = Pin(8)
D9 = Pin(9)
D10 = Pin(10)
D11 = Pin(11)
D12 = Pin(12)
D13 = Pin(13)
D14 = Pin(14)
D15 = Pin(15)
D16 = Pin(16)
D17 = Pin(17)
D18 = Pin(18)
D19 = Pin(19)
D20 = Pin(20)
D21 = Pin(21)
D22 = Pin(22)
D23 = Pin(23)
D24 = Pin(24)
D25 = Pin(25)
D26 = Pin(26)
D27 = Pin(27)
SDA_1 = Pin(27)
D28 = Pin(28)
SCL_1 = Pin(28)
D29 = Pin(29)
D30 = Pin(30)
D31 = Pin(31)
D32 = Pin(32)
D33 = Pin(33)
D34 = Pin(34)
D35 = Pin(35)
D36 = Pin(36)
D37 = Pin(37)
D38 = Pin(38)
D39 = Pin(39)
D40 = Pin(40)

i2cPorts = (
    (I2C_BUS, SCL, SDA), (I2C_BUS_1, SCL_1, SDA_1),
)

