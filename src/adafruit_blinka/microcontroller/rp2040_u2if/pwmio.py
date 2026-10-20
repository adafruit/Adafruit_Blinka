# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""PWMOut Class for RP2040s with u2if"""
from weakref import finalize

from .rp2040_u2if import rp2040_u2if


class PWMOut:
    """Base Pulse Width Modulation Output Class"""

    def __init__(self, pin, *, frequency=500, duty_cycle=0, variable_frequency=False):
        self._pin = pin
        # HID also uses weakref.finalize. This newer callback runs before its
        # native handle is closed, rather than accessing it from a late __del__.
        # Bind the backend, not self, so ordinary collection still releases PWM.
        self._finalizer = finalize(self, rp2040_u2if.pwm_deinit, pin)
        try:
            rp2040_u2if.pwm_configure(
                pin,
                frequency=frequency,
                duty_cycle=duty_cycle,
                variable_frequency=variable_frequency,
            )
        except BaseException:
            try:
                self.deinit()
            except Exception:  # pylint: disable=broad-except
                # A failed rollback must not hide the configuration error.
                pass
            raise

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self.deinit()

    def deinit(self):
        """Deinit PWM."""
        self._finalizer()

    def _check_for_deinit(self):
        if not self._finalizer.alive:
            raise ValueError("Object has been deinitialized and can no longer be used")

    @property
    def duty_cycle(self):
        """The PWM's output duty cycle, 16-bit."""
        self._check_for_deinit()
        return rp2040_u2if.pwm_get_duty_cycle(self._pin)

    @duty_cycle.setter
    def duty_cycle(self, duty_cycle):
        self._check_for_deinit()
        rp2040_u2if.pwm_set_duty_cycle(self._pin, duty_cycle)

    @property
    def frequency(self):
        """The PWM's output frequency in Hertz."""
        self._check_for_deinit()
        return rp2040_u2if.pwm_get_frequency(self._pin)

    @frequency.setter
    def frequency(self, frequency):
        self._check_for_deinit()
        rp2040_u2if.pwm_set_frequency(self._pin, frequency)
