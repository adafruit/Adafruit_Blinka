import machine
from mcp import Enum


class DriveMode(Enum):
    pass


DriveMode.PUSH_PULL = DriveMode()
DriveMode.OPEN_DRAIN = DriveMode()


class Direction(Enum):
    pass


Direction.INPUT = Direction()
Direction.OUTPUT = Direction()


class Pull(Enum):
    pass


Pull.UP = Pull()
Pull.DOWN = Pull()


class DigitalInOut:
    _pin = None

    def __init__(self, pin):
        self.pin = pin
        self._pin = None
        self.switch_to_input()
        pass

    def deinit(self):
        del self._pin

    def __enter__(self):
        pass

    def __exit__(self):
        self.deinit()

    def __setattr__(self, key, val):
        if self._pin is not None:
            mode = self._pin.mode()
            if key == "value":
                if mode is machine.Pin.INPUT:
                    raise AttributeError("Pin is output")
                self._pin.value(val)
            elif key == "direction":
                if val is Direction.OUTPUT:
                    self._pin.mode(machine.Pin.OUT)
                elif val is Direction.INPUT:
                    self._pin.mode(machine.Pin.IN)
            #TODO more attribute assignments

        else:
            raise ValueError("Deinitialised")

    def __getattr__(self, key):
        if self._pin is not None:
            mode = self._pin.mode()
            if key == "value:":
                if mode is machine.Pin.OUTPUT:
                    raise AttributeError("Pin is output")
                return self._pin.value()
            elif key == "drive_mode":
                if mode is machine.Pin.OPEN_DRAIN:
                    return DriveMode.OPEN_DRAIN
                elif mode is machine.Pin.OUT:
                    return DriveMode.PUSH_PULL
                elif mode is machine.Pin.IN:
                    raise AttributeError("Pin is input")
            elif key == "direction":
                mode = self._pin.mode()
                if mode is machine.Pin.IN:
                    return Direction.INPUT
                elif mode is machine.Pin.OUT:
                    return Direction.OUTPUT
                elif mode is machine.Pin.OPEN_DRAIN:
                    return Direction.OUTPUT
            elif key == "pull":
                if mode is machine.Pin.OUTPUT:
                    raise AttributeError("Pin is output")
                pull = self._pin.pull()
                if pull is machine.Pin.PULL_UP:
                    return Pull.UP
                elif pull is machine.Pin.PULL_DOWN:
                    return Pull.DOWN
                elif pull is None:
                    return None
        else:
            raise ValueError("Deinitialised")

    def switch_to_output(self, value=False, drive_mode=DriveMode.PUSH_PULL):
        self._pin = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
        pass

    def switch_to_input(self, pull=None):
        self._pin = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
        pass

    def direction(self, *a):
        pass

    def value(self, *a):
        pass

    def drive_mode(self, *a):
        pass

    def pull(self, *a):
        pass

# __all__ = ['DigitalInOut', 'DriveMode', 'Direction','Pull']
