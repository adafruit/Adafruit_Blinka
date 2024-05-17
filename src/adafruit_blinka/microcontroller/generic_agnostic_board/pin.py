# SPDX-FileCopyrightText: 2024 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""generic_agnostic_board pin interface"""
import random

class Pin:
    """A basic Pin class for use with generic_agnostic_board"""
    # pin modes
    OUT = 0
    IN = 1
    ADC = 2
    DAC = 3
    # pin values
    LOW = 0
    HIGH = 1

    expected_pin_behavior = {
      'Dx_INPUT_TRUE': return_true,
      'Dx_INPUT_FALSE': return_false,
      'Dx_INPUT_TRUE_THEN_FALSE': return_toggle,
      'Dx_INPUT_TRUE_PULL_UP': return_true,
      'Dx_INPUT_TRUE_PULL_DOWN': return_true,
      'Dx_OUTPUT_TRUE': return_true,
      'Dx_OUTPUT_FALSE': return_true,
      'Ax_INPUT_RAND_INT': return_random_int
    }

    def __init__(self, pin_id=None):
      self.id = pin_id
      self._mode = None
      self.previous_value = None
      self.current_value = None

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        if self.id is None:
            raise RuntimeError("Can not init a None type pin.")
        if pull is not None:
            raise NotImplementedError("Internal pullups and pulldowns not supported")
        self._mode = mode

    def write(self, new_value):
      """Saves the new_value to the pin for subsequent calls to .value"""
      self.previous_value = self.current_value
      self.current_value = new_value

    def read(self):
      """Returns the pin's expected value."""
      self.previous_value = self.current_value
      self.current_value = self.expected_pin_behavior.get(self.pin_id)
      return self.current_value

    def return_toggle(self):
      """Returns the pin's expected value, toggling between True and False"""
      toggle_state = not self.previous_value
      return toggle_state

    def return_false(self):
      """Returns the pin's expected value, False"""
      return False

    def return_true(self):
      """Returns the pin's expected value, True"""
      return True

    def return_random_int(self):
      """Returns a random integer"""
      return random.randint(0, 65535)

    def return_fixed_int_pi(self):
      """Returns the first five digits of Pi, 31415"""
      return 31415

    def value(self, val=None):
        """Set or return the Pin Value"""
        # Digital In / Out
        if self._mode in (Pin.IN, Pin.OUT):
            # digital read
            if val is None:
                return self.read()
            # digital write
            if val in (Pin.LOW, Pin.HIGH):
                return self.write(val)
            # nope
            raise ValueError("Invalid value for pin.")
        # Analog In
        if self._mode == Pin.ADC:
            if val is None:
                return self.read()
            # read only
            raise AttributeError("'AnalogIn' object has no attribute 'value'")
        # Analog Out
        if self._mode == Pin.DAC:
            if val is None:
                # write only
                raise AttributeError("unreadable attribute")
            self.write(val)
            return None
        raise RuntimeError(
            "No action for mode {} with value {}".format(self._mode, val)
        )
