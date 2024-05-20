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

    def __init__(self, pin_id=None):
        self.id = pin_id
        self._mode = None
        self.previous_value = None
        self.current_value = None

        # mapping of pin definition names to expected behavior
        self.pin_behavior = {
            0: self.return_true,  # Dx_INPUT_TRUE
            1: self.return_false,  # Dx_INPUT_FALSE
            2: self.return_true,  # Dx_INPUT_TRUE_PULL_UP
            3: self.return_true,  # Dx_INPUT_TRUE_PULL_DOWN
            4: self.return_true,  # Dx_OUTPUT_TRUE
            5: self.return_false,  # Dx_OUTPUT_FALSE
            6: self.return_true,  # NEOPIXEL
            7: self.return_random_int,  # Ax_INPUT_RAND_INT
            8: self.return_fixed_int_pi,  # Ax_INPUT_FIXED_INT_PI
            9: self.return_true,  # Ax_OUTPUT_WAVE_SINE
            10: self.return_true,  # Ax_OUTPUT_WAVE_SAWTOOTH
            # Add other mappings as needed
        }

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
        # perform a lookup on the pin_behavior dict to get the value
        self.current_value = self.pin_behavior.get(self.id)()
        return self.current_value

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


# create pin instances for each pin
D0 = Pin(0)
D1 = Pin(1)
D2 = Pin(2)
D3 = Pin(3)
D4 = Pin(4)
D5 = Pin(5)
# Special "digital" pins
D6 = Pin(6)
# Analog pins
A0 = Pin(7)
A1 = Pin(8)
A2 = Pin(9)
A3 = Pin(10)

# I2C pins
SDA = Pin()
SCL = Pin()

# SPI pins
SCLK = Pin()
SCK = Pin()
MOSI = Pin()
MISO = Pin()
CS = Pin()

# UART pins
UART_TX = Pin()
UART_RX = Pin()
