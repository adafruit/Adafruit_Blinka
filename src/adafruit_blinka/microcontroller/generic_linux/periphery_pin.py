# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""A Pin class for use with periphery."""
try:
    from periphery import GPIO
except ImportError:
    raise ImportError(
        "Periphery Python bindings not found, please install and try again! "
        "Try running 'pip3 install python-periphery'"
    ) from ImportError


class Pin:
    """Pins dont exist in CPython so...lets make our own!"""

    IN = "in"
    OUT = "out"
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2

    id = None
    _value = LOW
    _mode = IN

    def __init__(self, pin_id):
        self.id = pin_id
        if isinstance(pin_id, tuple):
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
        """Initialize the Pin"""
        if mode is not None:
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

            if pull is not None:
                if pull == self.PULL_UP:
                    raise NotImplementedError(
                        "Internal pullups not supported in periphery, "
                        "use physical resistor instead!"
                    )
                if pull == self.PULL_DOWN:
                    raise NotImplementedError(
                        "Internal pulldowns not supported in periphery, "
                        "use physical resistor instead!"
                    )
                raise RuntimeError("Invalid pull for pin: %s" % self.id)

    def value(self, val=None):
        """Set or return the Pin Value"""
        if val is not None:
            if val == self.LOW:
                self._value = val
                self._line.write(False)
                return None
            if val == self.HIGH:
                self._value = val
                self._line.write(True)
                return None
            raise RuntimeError("Invalid value for pin")
        return self.HIGH if self._line.read() else self.LOW
