"""
`analogio` - Analog input and output control
=================================================
See `CircuitPython:analogio` in CircuitPython for more details.
* Author(s): Carter Nelson
"""

from adafruit_blinka.agnostic import board_id, detector

# pylint: disable=ungrouped-imports,wrong-import-position

if detector.board.microchip_mcp2221:
    from adafruit_blinka.microcontroller.mcp2221.pin import Pin
else:
    raise NotImplementedError("analogio not supported for this board.")

from adafruit_blinka import ContextManaged

class AnalogIn(ContextManaged):

    def __init__(self, pin):
        self._pin = Pin(pin.id)
        self._pin.init(mode=Pin.ADC)

    @property
    def value(self):
        return self._pin.value()

    @value.setter
    def value(self, value):
        # emulate what CircuitPython does
        raise AttributeError("'AnalogIn' object has no attribute 'value'")

    def deinit(self):
        del self._pin

class AnalogOut(ContextManaged):
    def __init__(self, pin):
        self._pin = Pin(pin.id)
        self._pin.init(mode=Pin.DAC)

    @property
    def value(self):
        # emulate what CircuitPython does
        raise AttributeError("unreadable attribute")

    @value.setter
    def value(self, value):
        self._pin.value(value)

    def deinit(self):
        del self._pin