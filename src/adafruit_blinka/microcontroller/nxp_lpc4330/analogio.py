"""
`analogio` - Analog input and output control
=================================================
See `CircuitPython:analogio` in CircuitPython for more details.
* Author(s): Carter Nelson
"""

from adafruit_blinka.microcontroller.nxp_lpc4330.pin import Pin
from adafruit_blinka import ContextManaged


class AnalogIn(ContextManaged):
    """Analog Input Class"""

    def __init__(self, pin):
        self._pin = Pin(pin.id)
        self._pin.init(mode=Pin.ADC)

    @property
    def value(self):
        """Read the ADC and return the value"""
        return self._pin.value()

    # pylint: disable=no-self-use
    @value.setter
    def value(self, value):
        # emulate what CircuitPython does
        raise AttributeError("'AnalogIn' object has no attribute 'value'")

    # pylint: enable=no-self-use

    def deinit(self):
        del self._pin


class AnalogOut(ContextManaged):
    """Analog Output Class"""

    def __init__(self, pin):
        self._pin = Pin(pin.id)
        self._pin.init(mode=Pin.DAC)

    @property
    def value(self):
        """Return an error. This is output only."""
        # emulate what CircuitPython does
        raise AttributeError("unreadable attribute")

    @value.setter
    def value(self, value):
        self._pin.value(value)

    def deinit(self):
        del self._pin
