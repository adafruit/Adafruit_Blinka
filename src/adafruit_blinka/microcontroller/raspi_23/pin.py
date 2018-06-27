import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

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

SDA = Pin(2)
SCL = Pin(3)
D2 = Pin(2)
D3 = Pin(3)
D4 = Pin(4)
D9 = Pin(9)
D10 = Pin(10)
D11 = Pin(11)
MISO = Pin(9)
MOSI = Pin(10)
SCLK = Pin(11)
D14 = Pin(14)
D15 = Pin(15)
TXD = Pin(14)
RXD = Pin(15)
D17 = Pin(17)
D18 = Pin(18)
D19 = Pin(19)
D20 = Pin(20)
MISO_2 = Pin(19)
MOSI_2 = Pin(20)
SCLK_2 = Pin(21)
D21 = Pin(21)
D22 = Pin(22)
D23 = Pin(23)
D24 = Pin(24)
D27 = Pin(27)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SCLK, MOSI, MISO), (1, SCLK_2, MOSI_2, MISO_2))

# ordered as uartId, txId, rxId
uartPorts = (
    (1, TXD, RXD),
)

i2cPorts = (
    (1, SCL, SDA),
)

