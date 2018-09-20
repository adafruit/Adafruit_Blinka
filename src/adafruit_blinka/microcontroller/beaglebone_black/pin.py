import Adafruit_BBIO.GPIO as GPIO

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
    
    def __init__(self, pin_name):
        self.id = pin_name

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

P8_3 = Pin('P8_3')
P8_4 = Pin('P8_4')
P8_5 = Pin('P8_5')
P8_6 = Pin('P8_6')
P8_7 = Pin('P8_7')
P8_8 = Pin('P8_8')
P8_9 = Pin('P8_9')
P8_10 = Pin('P8_10')
P8_11 = Pin('P8_11')
P8_12 = Pin('P8_12')
P8_13 = Pin('P8_13')
P8_14 = Pin('P8_14')
P8_15 = Pin('P8_15')
P8_16 = Pin('P8_16')
P8_17 = Pin('P8_17')
P8_18 = Pin('P8_18')
P8_19 = Pin('P8_19')
P8_20 = Pin('P8_20')
P8_21 = Pin('P8_21')
P8_22 = Pin('P8_22')
P8_23 = Pin('P8_23')
P8_24 = Pin('P8_24')
P8_25 = Pin('P8_25')
P8_26 = Pin('P8_26')
P8_27 = Pin('P8_27')
P8_28 = Pin('P8_28')
P8_29 = Pin('P8_29')
P8_30 = Pin('P8_30')
P8_31 = Pin('P8_31')
P8_32 = Pin('P8_32')
P8_33 = Pin('P8_33')
P8_34 = Pin('P8_34')
P8_35 = Pin('P8_35')
P8_36 = Pin('P8_36')
P8_37 = Pin('P8_37')
P8_38 = Pin('P8_38')
P8_39 = Pin('P8_39')
P8_40 = Pin('P8_40')
P8_41 = Pin('P8_41')
P8_42 = Pin('P8_42')
P8_43 = Pin('P8_43')
P8_44 = Pin('P8_44')
P8_45 = Pin('P8_45')
P8_46 = Pin('P8_46')
P9_11 = Pin('P9_11')
P9_12 = Pin('P9_12')
P9_13 = Pin('P9_13')
P9_14 = Pin('P9_14')
P9_15 = Pin('P9_15')
P9_16 = Pin('P9_16')
P9_17 = Pin('P9_17')
P9_18 = Pin('P9_18')
P9_19 = Pin('P9_19')
P9_20 = Pin('P9_20')
P9_21 = Pin('P9_21')
P9_22 = Pin('P9_22')
P9_23 = Pin('P9_23')
P9_24 = Pin('P9_24')
P9_25 = Pin('P9_25')
P9_26 = Pin('P9_26')
P9_27 = Pin('P9_27')
P9_28 = Pin('P9_28')
P9_29 = Pin('P9_29')
P9_30 = Pin('P9_30')
P9_31 = Pin('P9_31')
P9_41 = Pin('P9_41')
P9_42 = Pin('P9_42')

USR0 = Pin('USR0')
USR1 = Pin('USR1')
USR2 = Pin('USR2')
USR3 = Pin('USR3')

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ()

# ordered as uartId, txId, rxId
uartPorts = (
    (),
)

i2cPorts = (
    (),
)

