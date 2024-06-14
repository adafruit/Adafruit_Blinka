# SPDX-FileCopyrightText: 2024 Brent Rubell for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Mock PWMOut Wrapper for Generic Agnostic Board"""


class PWMError(IOError):
    """Base class for PWM errors."""


class PWMOut:
    """Pulse Width Modulation Output Class"""

    def __init__(self, pin, *, frequency=500, duty_cycle=0, variable_frequency=False):
        self._pwmpin = None
        self._period = 0
        self._open(pin, duty_cycle, frequency, variable_frequency)

    def __del__(self):
        self.deinit()

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self.deinit()

    def _open(self, pin, duty=0, freq=500, variable_frequency=False):
        self._pin = pin

        # set frequency
        self.frequency = freq
        self._variable_frequency = variable_frequency
        # set duty
        self.duty_cycle = duty

        self.enabled = True

    def deinit(self):
        """Deinit the PWM."""
        if self._pwmpin is not None:
            self._pwmpin = None

    def _is_deinited(self):
        if self._pwmpin is None:
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
            raise TypeError("Invalid enabled type, should be string.")

        self._enabled = value

    # String representation
    def __str__(self):
        return "pin %s (freq=%f Hz, duty_cycle=%f%%)" % (
            self._pin,
            self.frequency,
            self.duty_cycle,
        )
