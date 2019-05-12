try:
    import gpiod
except ImportError:
    raise ImportError("libgpiod Python bindings not found, please install and try again! See https://github.com/adafruit/Raspberry-Pi-Installer-Scripts/blob/master/libgpiod.sh")

# Pins dont exist in CPython so...lets make our own!
class Pin:
    IN = 0
    OUT = 1
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
            self._chip = gpiod.Chip(str(pin_id[0]), gpiod.Chip.OPEN_BY_NUMBER)
        else:
            self._num = int(pin_id)
            self._chip = gpiod.Chip("gpiochip0", gpiod.Chip.OPEN_BY_NAME)
        self._line = None

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        if not self._line:
            self._line = self._chip.get_line(int(self._num))
            #print("init line: ", self.id, self._line)

        if mode != None:
            if mode == self.IN:
                flags = 0
                if pull != None:
                    if pull == self.PULL_UP:
                        raise NotImplementedError("Internal pullups not supported in libgpiod, use physical resistor instead!")
                    elif pull == self.PULL_DOWN:
                        raise NotImplementedError("Internal pulldowns not supported in libgpiod, use physical resistor instead!")                    
                    else:
                        raise RuntimeError("Invalid pull for pin: %s" % self.id)

                self._mode = self.IN
                self._line.release()
                self._line.request(consumer=self._CONSUMER,
                                   type=gpiod.LINE_REQ_DIR_IN,
                                   flags=flags)

            elif mode == self.OUT:
                if pull != None:
                    raise RuntimeError("Cannot set pull resistor on output")
                self._mode = self.OUT
                self._line.release()
                self._line.request(consumer=self._CONSUMER,
                                   type=gpiod.LINE_REQ_DIR_OUT)

            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)

    def value(self, val=None):
        if val != None:
            if val in (self.LOW, self.HIGH):
                self._value = val
                self._line.set_value(val)
            else:
                raise RuntimeError("Invalid value for pin")
        else:
            return self._line.get_value()
