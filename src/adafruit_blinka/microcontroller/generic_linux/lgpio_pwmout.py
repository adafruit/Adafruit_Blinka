# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

""" PWMOut Class for lgpio lg library tx_pwm library """

import lgpio
from adafruit_blinka.microcontroller.generic_linux.lgpio_pin import CHIP


class PWMError(IOError):
    """Base class for PWM errors."""


class PWMOut:
    """Pulse Width Modulation Output Class"""

    def __init__(self, pin, *, frequency=500, duty_cycle=0, variable_frequency=False):
        if variable_frequency:
            print("Variable Frequency is not supported, ignoring...")
        self._pin = pin
        result = lgpio.gpio_claim_output(CHIP, self._pin.id, lFlags=lgpio.SET_PULL_NONE)
        if result < 0:
            raise RuntimeError(lgpio.error_text(result))
        self._enabled = False
        self._deinited = False
        self._period = 0
        # set frequency
        self._frequency = frequency
        # set duty
        self.duty_cycle = duty_cycle
        self.enabled = True

    def __del__(self):
        self.deinit()

    def __enter__(self):
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        self.deinit()

    def deinit(self):
        """Deinit the PWM."""
        if not self._deinited:
            if self.enabled:
                self._enabled = False  # turn off the pwm
            self._deinited = True

    def _is_deinited(self):
        """raise Value error if the object has been de-inited"""
        if self._deinited:
            raise ValueError(
                "Object has been deinitialize and can no longer "
                "be used. Create a new object."
            )

    @property
    def period(self):
        """Get or set the PWM's output period in seconds.

        Raises:
            PWMError: if an I/O or OS error occurs.
            TypeError: if value type is not int or float.

        :type: int, float
        """
        return 1.0 / self.frequency

    @period.setter
    def period(self, period):
        if not isinstance(period, (int, float)):
            raise TypeError("Invalid period type, should be int or float.")

        self.frequency = 1.0 / period

    @property
    def duty_cycle(self):
        """Get or set the PWM's output duty cycle which is the fraction of
        each pulse which is high. 16-bit

        Raises:
            PWMError: if an I/O or OS error occurs.
            TypeError: if value type is not int or float.
            ValueError: if value is out of bounds of 0.0 to 1.0.

        :type: int, float
        """
        return int(self._duty_cycle * 65535)

    @duty_cycle.setter
    def duty_cycle(self, duty_cycle):
        if not isinstance(duty_cycle, (int, float)):
            raise TypeError("Invalid duty cycle type, should be int or float.")

        if not 0 <= duty_cycle <= 65535:
            raise ValueError("Invalid duty cycle value, should be between 0 and 65535")

        # convert from 16-bit
        duty_cycle /= 65535.0

        self._duty_cycle = duty_cycle
        if self._enabled:
            self.enabled = True  # turn on with new values

    @property
    def frequency(self):
        """Get or set the PWM's output frequency in Hertz.

        Raises:
            PWMError: if an I/O or OS error occurs.
            TypeError: if value type is not int or float.

        :type: int, float
        """

        return self._frequency

    @frequency.setter
    def frequency(self, frequency):
        if not isinstance(frequency, (int, float)):
            raise TypeError("Invalid frequency type, should be int or float.")

        self._frequency = frequency
        if self.enabled:
            self.enabled = True  # turn on with new values

    @property
    def enabled(self):
        """Get or set the PWM's output enabled state.

        Raises:
            PWMError: if an I/O or OS error occurs.
            TypeError: if value type is not bool.

        :type: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if not isinstance(value, bool):
            raise TypeError("Invalid enabled type, should be bool.")

        frequency = self._frequency if value else 0
        duty_cycle = round(self._duty_cycle * 100)
        self._enabled = value
        result = lgpio.tx_pwm(CHIP, self._pin.id, frequency, duty_cycle)
        if result < 0:
            raise RuntimeError(lgpio.error_text(result))
        return result

    # String representation
    def __str__(self):
        return (
            f"pin {self._pin} (freq={self.frequency:f} Hz, duty_cycle="
            f"{self.duty_cycle}({round(self.duty_cycle / 655.35)}%)"
        )
