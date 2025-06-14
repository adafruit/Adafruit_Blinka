# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`analogio` - Analog input and output control
=================================================
See `CircuitPython:analogio` in CircuitPython for more details.
* Author(s): Carter Nelson
"""
from adafruit_blinka import ContextManaged
from .rp2040_u2if import rp2040_u2if


class AnalogIn(ContextManaged):
    """AnalogIn Base Class for RP2040 u2if"""

    def __init__(self, pin):
        self.pin_id = pin.id
        rp2040_u2if.adc_init_pin(self.pin_id)

    @property
    def value(self):
        """Read the ADC and return the value"""
        return rp2040_u2if.adc_get_value(self.pin_id) << 4

    # pylint: disable=no-self-use
    @value.setter
    def value(self, value):
        # emulate what CircuitPython does
        raise AttributeError("'AnalogIn' object has no attribute 'value'")

    # pylint: enable=no-self-use

    def deinit(self):
        pass


class AnalogIn_Pico(AnalogIn):
    """AnalogIn Base Class for Pico u2if"""

    def __init__(self, pin):
        # per their pinout, why only two?
        if pin.id not in (26, 27):
            raise ValueError("Pin does not support ADC.")
        super().__init__(pin)


class AnalogIn_Feather(AnalogIn):
    """AnalogIn Base Class for Feather u2if"""

    def __init__(self, pin):
        if pin.id not in (26, 27, 28):
            raise ValueError("Pin does not support ADC.")
        super().__init__(pin)


class AnalogIn_QTPY(AnalogIn):
    """AnalogIn Base Class for QT Py 2040 u2if"""

    def __init__(self, pin):
        if pin.id not in (26, 27, 28):
            raise ValueError("Pin does not support ADC.")
        super().__init__(pin)


class AnalogIn_ItsyBitsy(AnalogIn):
    """AnalogIn Base Class for ItsyBitsy 2040 u2if"""

    def __init__(self, pin):
        if pin.id not in (26, 27, 28):
            raise ValueError("Pin does not support ADC.")
        super().__init__(pin)


class AnalogIn_Radxa_X4(AnalogIn):
    """AnalogIn Base Class for Radxa X4 u2if"""

    def __init__(self, pin):
        if pin.id not in (26, 27, 28, 29):
            raise ValueError("Pin does not support ADC.")
        super().__init__(pin)
