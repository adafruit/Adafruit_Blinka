import gpiod
# GPIO.setmode(GPIO.BCM)    # Use BCM pins D4 = GPIO #4
# GPIO.setwarnings(False)   # shh!

# Pins dont exist in CPython so...lets make our own!
class Pin:
    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2
    _CONSUMER = 'Adafruit-Blinka'

    id = None
    _value = LOW
    _mode = IN

    def __init__(self, pin_number):
        self.id = pin_number
        self._chip = gpiod.Chip("gpiochip0") # FIXME presumably varies by system?
        self._line = self._chip.get_line(int(pin_number))

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        if mode != None:
            if mode == self.IN:
                self._mode = self.IN
                self._line.request(consumer=self._CONSUMER, type=gpiod.LINE_REQ_DIR_IN)
                # GPIO.setup(self.id, GPIO.IN)
            elif mode == self.OUT:
                self._mode = self.OUT
                self._line.request(consumer=self._CONSUMER, type=gpiod.LINE_REQ_DIR_OUT)
                # GPIO.setup(self.id, GPIO.OUT)
            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)
        if pull != None:
            if self._mode != self.IN:
                raise RuntimeError("Cannot set pull resistor on output")
            if pull == self.PULL_UP:
                GPIO.setup(self.id, GPIO.IN, pull_up_down=GPIO.PUD_UP) # XXX
            elif pull == self.PULL_DOWN:
                GPIO.setup(self.id, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # XXX
            else:
                raise RuntimeError("Invalid pull for pin: %s" % self.id)       

    def value(self, val=None):
        if val != None:
            if val in (self.LOW, self.HIGH):
                self._value = val
                self._line.set_value(val)
                # GPIO.output(self.id, val)
            else:
                raise RuntimeError("Invalid value for pin")
        else:
            return self._line.get_value()
            # return GPIO.input(self.id)
