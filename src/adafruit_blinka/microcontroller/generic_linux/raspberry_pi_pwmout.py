# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Blinka's legacy PWM surface over the strict Raspberry Pi PWM package.

Frequency readback retains the requested value, as the RPi.GPIO wrapper does.
The native engine receives a nearest-integer frequency and integer duty cycle;
this adapter does not extend its 1..10000 Hz configuration range. Disabling
requests LOW at the native update boundary without releasing the owned line.
"""

import math

from adafruit_blinka_raspberry_pi_pwm import PWMOut as _NativePWMOut


def _number(value, name):
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be int or float")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _frequency(value):
    value = _number(value, "frequency")
    effective = round(value)
    if not 1 <= effective <= 10000:
        raise ValueError("frequency must round to an integer between 1 and 10000 Hz")
    return effective


def _duty(value):
    value = _number(value, "duty_cycle")
    if not 0 <= value <= 65535:
        raise ValueError("duty_cycle must be between 0 and 65535")
    return int(value)


class PWMOut:
    """Compatibility adapter; frequency remains writable regardless of its flag.

    ``variable_frequency`` is accepted for compatibility with the original
    wrappers. The underlying native output always enables frequency changes.
    ``enabled`` describes requested output state, not an electrical readback.
    """

    def __init__(self, pin, *, frequency=500, duty_cycle=0, variable_frequency=False):
        _ = variable_frequency  # Legacy wrappers permit writes regardless of this flag.
        self._pwm = None
        self._enabled = False
        effective = _frequency(frequency)
        duty = _duty(duty_cycle)
        # Retain a partially initialized native object so cleanup is attempted
        # even when its constructor raises. Never replace the primary error.
        native = _NativePWMOut.__new__(_NativePWMOut)
        self._pwm = native
        try:
            _NativePWMOut.__init__(
                native,
                pin,
                frequency=effective,
                duty_cycle=duty,
                variable_frequency=True,
            )
        except BaseException:
            try:
                self.deinit()
            except BaseException:  # pylint: disable=broad-except
                pass
            raise
        self._frequency = frequency
        self._duty_cycle = duty_cycle
        self._enabled = True

    def _check(self):
        if self._pwm is None:
            raise ValueError("Object has been deinitialized")
        # A public native read also reports asynchronous worker failures.
        _ = self._pwm.frequency
        return self._pwm

    @property
    def frequency(self):
        """Requested frequency; the engine uses round(value) Hz, within 1..10000."""
        self._check()
        return self._frequency

    @frequency.setter
    def frequency(self, value):
        native = self._check()
        effective = _frequency(value)
        native.frequency = effective
        self._frequency = value

    @property
    def duty_cycle(self):
        """Requested 16-bit duty, truncated to an integer on submission/readback."""
        self._check()
        return int(self._duty_cycle)

    @duty_cycle.setter
    def duty_cycle(self, value):
        native = self._check()
        duty = _duty(value)
        if self._enabled:
            native.duty_cycle = duty
        self._duty_cycle = value

    @property
    def period(self):
        """Requested period in seconds, the reciprocal of requested frequency."""
        return 1.0 / self.frequency

    @period.setter
    def period(self, value):
        self._check()
        value = _number(value, "period")
        if value <= 0:
            raise ValueError("period must be positive")
        self.frequency = 1 / value

    @property
    def enabled(self):
        """Whether PWM is requested, independent of its saved duty-cycle value."""
        self._check()
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        native = self._check()
        if not isinstance(value, bool):
            raise TypeError("enabled must be bool")
        native.duty_cycle = int(self._duty_cycle) if value else 0
        self._enabled = value

    def deinit(self):
        """Join the native worker, drive LOW and release this output; repeat-safe."""
        native = self._pwm
        self._pwm = None
        self._enabled = False
        if native is not None:
            native.deinit()

    def __enter__(self):
        self._check()
        return self

    def __exit__(self, _exc_type, _exc_value, _traceback):
        self.deinit()

    def __del__(self):
        try:
            self.deinit()
        except Exception:  # pylint: disable=broad-except
            # Explicit deinit reports errors; finalizers cannot do so reliably.
            pass
