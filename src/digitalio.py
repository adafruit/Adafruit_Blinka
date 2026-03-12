# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`digitalio` - Digital input and output control (GPIO)
=====================================================

See `CircuitPython:digitalio` in CircuitPython for more details.

* Author(s): cefn, Melissa LeBlanc-Williams
"""
import json
from adafruit_blinka.agnostic import board_id
from adafruit_blinka.importing import get_import_file, import_microcontroller
from adafruit_blinka import Enum, ContextManaged

Pin = None

with open(get_import_file("microcontroller_imports.json", __file__)) as f:
    microcontroller_imports = json.load(f)
    import_microcontroller(globals(), microcontroller_imports, "pin", "Pin")


class DriveMode(Enum):
    """Drive Mode Enumeration"""

    PUSH_PULL = None
    OPEN_DRAIN = None


DriveMode.PUSH_PULL = DriveMode()
DriveMode.OPEN_DRAIN = DriveMode()


class Direction(Enum):
    """Direction Enumeration"""

    INPUT = None
    OUTPUT = None


Direction.INPUT = Direction()
Direction.OUTPUT = Direction()


class Pull(Enum):
    """PullUp/PullDown Enumeration"""

    UP = None
    DOWN = None
    # NONE=None


Pull.UP = Pull()
Pull.DOWN = Pull()

# Pull.NONE = Pull()


class DigitalInOut(ContextManaged):
    """DigitalInOut CircuitPython compatibility implementation"""

    _pin = None

    def __init__(self, pin):
        self._pin = Pin(pin.id)  # pylint: disable=not-callable
        self.direction = Direction.INPUT

    def switch_to_output(self, value=False, drive_mode=DriveMode.PUSH_PULL):
        """Switch the Digital Pin Mode to Output"""
        self.direction = Direction.OUTPUT
        self.value = value
        self.drive_mode = drive_mode

    def switch_to_input(self, pull=None):
        """Switch the Digital Pin Mode to Input"""
        self.direction = Direction.INPUT
        self.pull = pull

    def deinit(self):
        """Deinitialize the Digital Pin"""
        del self._pin

    @property
    def direction(self):
        """Get or Set the Digital Pin Direction"""
        return self.__direction

    @direction.setter
    def direction(self, value):
        self.__direction = value
        if value is Direction.OUTPUT:
            self._pin.init(mode=Pin.OUT)
            self.value = False
            self.drive_mode = DriveMode.PUSH_PULL
        elif value is Direction.INPUT:
            self._pin.init(mode=Pin.IN)
            self.pull = None
        else:
            raise AttributeError("Not a Direction")

    @property
    def value(self):
        """The Digital Pin Value"""
        return self._pin.value() == 1

    @value.setter
    def value(self, val):
        if self.direction is Direction.OUTPUT:
            self._pin.value(1 if val else 0)
        else:
            raise AttributeError("Not an output")

    @property
    def pull(self):
        """The pin pull direction"""
        if self.direction is Direction.INPUT:
            return self.__pull
        raise AttributeError("Not an input")

    @pull.setter
    def pull(self, pul):
        if self.direction is Direction.INPUT:
            self.__pull = pul
            if pul is Pull.UP:
                self._pin.init(mode=Pin.IN, pull=Pin.PULL_UP)
            elif pul is Pull.DOWN:
                if hasattr(Pin, "PULL_DOWN"):
                    self._pin.init(mode=Pin.IN, pull=Pin.PULL_DOWN)
                else:
                    raise NotImplementedError(
                        "{} unsupported on {}".format(Pull.DOWN, board_id)
                    )
            elif pul is None:
                self._pin.init(mode=Pin.IN, pull=None)
            else:
                raise AttributeError("Not a Pull")
        else:
            raise AttributeError("Not an input")

    @property
    def drive_mode(self):
        """The Digital Pin Drive Mode"""
        if self.direction is Direction.OUTPUT:
            return self.__drive_mode  #
        raise AttributeError("Not an output")

    @drive_mode.setter
    def drive_mode(self, mod):
        self.__drive_mode = mod
        if mod is DriveMode.OPEN_DRAIN:
            self._pin.init(mode=Pin.OPEN_DRAIN)
        elif mod is DriveMode.PUSH_PULL:
            self._pin.init(mode=Pin.OUT)
