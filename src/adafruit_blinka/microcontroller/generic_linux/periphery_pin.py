try:
    from periphery import GPIO
except ImportError:
    raise ImportError("Periphery Python bindings not found, please install and try again! Try running 'pip3 install python-periphery'")

# Pins dont exist in CPython so...lets make our own!
class Pin:
    IN = "in"
    OUT = "out"
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2
    _CONSUMER = 'adafruit_blinka'

    id = None
    _value = LOW
    _mode = IN

    def __init__(self, pin_id):
        self.id = pin_id
        if type(pin_id) is tuple:
            self._num = int(pin_id[1])
            self._chippath = "/dev/gpiochip{}".format(pin_id[0])
        else:
            self._num = int(pin_id)
            self._chippath = "/dev/gpiochip0"
        self._line = None

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        if mode != None:
            if mode == self.IN:
                self._mode = self.IN
                if self._line is not None:
                    self._line.close()
                self._line = GPIO(self._chippath, int(self._num), self.IN)
            elif mode == self.OUT:
                self._mode = self.OUT
                if self._line is not None:
                    self._line.close()
                self._line = GPIO(self._chippath, int(self._num), self.OUT)
            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)

            if pull != None:
                if pull == self.PULL_UP:
                    raise NotImplementedError("Internal pullups not supported in periphery, use physical resistor instead!")
                elif pull == self.PULL_DOWN:
                    raise NotImplementedError("Internal pulldowns not supported in periphery, use physical resistor instead!")
                else:
                    raise RuntimeError("Invalid pull for pin: %s" % self.id)

    def value(self, val=None):
        if val != None:
            if val == self.LOW:
                self._value = val
                self._line.write(False)
            elif val == self.HIGH:
                self._value = val
                self._line.write(True)
            else:
                raise RuntimeError("Invalid value for pin")
        else:
            return self.HIGH if self._line.read() else self.LOW

