"""
`analogio` - Analog input and output control
=================================================
See `CircuitPython:analogio` in CircuitPython for more details.
* Author(s): Carter Nelson
"""
from adafruit_blinka import ContextManaged
from .pico_u2if import pico_u2if


class AnalogIn(ContextManaged):
    """Analog Input Class"""

    def __init__(self, pin):
        # per their pinout, why only two?
        if pin.id not in (26, 27):
            raise ValueError("Pin does not support ADC.")
        self.pin_id = pin.id
        pico_u2if.adc_init_pin(self.pin_id)

    @property
    def value(self):
        """Read the ADC and return the value"""
        return pico_u2if.adc_get_value(self.pin_id) << 4

    # pylint: disable=no-self-use
    @value.setter
    def value(self, value):
        # emulate what CircuitPython does
        raise AttributeError("'AnalogIn' object has no attribute 'value'")

    # pylint: enable=no-self-use

    def deinit(self):
        pass
