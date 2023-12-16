# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Much code from https://github.com/vsergeev/python-periphery/blob/master/periphery/pwm.py
Copyright (c) 2015-2016 vsergeev / Ivan (Vanya) A. Sergeev
License: MIT
"""

import os
from time import sleep
from errno import EACCES

try:
    from microcontroller.pin import pwmOuts
except ImportError:
    raise RuntimeError("No PWM outputs defined for this board") from ImportError


# pylint: disable=unnecessary-pass
class PWMError(IOError):
    """Base class for PWM errors."""

    pass


# pylint: enable=unnecessary-pass


class PWMOut:
    """Pulse Width Modulation Output Class"""

    # Number of retries to check for successful PWM export on open
    PWM_STAT_RETRIES = 10
    # Delay between check for scucessful PWM export on open (100ms)
    PWM_STAT_DELAY = 0.1

    # Sysfs paths
    _sysfs_path = "/sys/class/pwm/"
    _channel_path = "pwmchip{}"

    # Channel paths
    _export_path = "export"
    _unexport_path = "unexport"
    _pin_path = "pwm{}"

    # Pin attribute paths
    _pin_period_path = "period"
    _pin_duty_cycle_path = "duty_cycle"
    _pin_polarity_path = "polarity"
    _pin_enable_path = "enable"

    def __init__(self, pin, *, frequency=500, duty_cycle=0, variable_frequency=False):
        """Instantiate a PWM object and open the sysfs PWM corresponding to the
        specified channel and pin.

        Args:
            pin (Pin): CircuitPython Pin object to output to
            duty_cycle (int) : The fraction of each pulse which is high. 16-bit
            frequency (int) : target frequency in Hertz (32-bit)
            variable_frequency (bool) : True if the frequency will change over time

        Returns:
            PWMOut: PWMOut object.

        Raises:
            PWMError: if an I/O or OS error occurs.
            TypeError: if `channel` or `pin` types are invalid.
            ValueError: if PWM channel does not exist.

        """

        self._pwmpin = None
        self._channel = None
        self._period = 0
        self._open(pin, duty_cycle, frequency, variable_frequency)

    def __del__(self):
        self.deinit()

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self.deinit()

    def _open(self, pin, duty=0, freq=500, variable_frequency=False):
        self._channel = None
        for pwmpair in pwmOuts:
            if pwmpair[1] == pin:
                self._channel = pwmpair[0][0]
                self._pwmpin = pwmpair[0][1]

        self._pin = pin
        if self._channel is None:
            raise RuntimeError("No PWM channel found for this Pin")

        if variable_frequency:
            print("Variable Frequency is not supported, continuing without it...")

        channel_path = os.path.join(
            self._sysfs_path, self._channel_path.format(self._channel)
        )
        if not os.path.isdir(channel_path):
            raise ValueError(
                "PWM channel does not exist, check that the required modules are loaded."
            )

        try:
            with open(
                os.path.join(channel_path, self._unexport_path), "w", encoding="utf-8"
            ) as f_unexport:
                f_unexport.write("%d\n" % self._pwmpin)
        except IOError:
            pass  # not unusual, it doesnt already exist
        try:
            with open(
                os.path.join(channel_path, self._export_path), "w", encoding="utf-8"
            ) as f_export:
                f_export.write("%d\n" % self._pwmpin)
        except IOError as e:
            raise PWMError(e.errno, "Exporting PWM pin: " + e.strerror) from IOError

        # Loop until 'period' is writable, because application of udev rules
        # after the above pin export is asynchronous.
        # Without this loop, the following properties may not be writable yet.
        for i in range(PWMOut.PWM_STAT_RETRIES):
            try:
                with open(
                    os.path.join(
                        channel_path, self._pin_path.format(self._pwmpin), "period"
                    ),
                    "w",
                    encoding="utf-8",
                ):
                    break
            except IOError as e:
                if e.errno != EACCES or (
                    e.errno == EACCES and i == PWMOut.PWM_STAT_RETRIES - 1
                ):
                    raise PWMError(e.errno, "Opening PWM period: " + e.strerror) from e
            sleep(PWMOut.PWM_STAT_DELAY)

        # self._set_enabled(False) # This line causes a write error when trying to enable

        # Look up the period, for fast duty cycle updates
        self._period = self._get_period()

        # self.duty_cycle = 0  # This line causes a write error when trying to enable

        # set frequency
        self.frequency = freq
        # set duty
        self.duty_cycle = duty

        self._set_enabled(True)

    def deinit(self):
        """Deinit the sysfs PWM."""
        if self._channel is not None:
            try:
                channel_path = os.path.join(
                    self._sysfs_path, self._channel_path.format(self._channel)
                )
                with open(
                    os.path.join(channel_path, self._unexport_path),
                    "w",
                    encoding="utf-8",
                ) as f_unexport:
                    f_unexport.write("%d\n" % self._pwmpin)
            except IOError as e:
                raise PWMError(
                    e.errno, "Unexporting PWM pin: " + e.strerror
                ) from IOError

        self._channel = None
        self._pwmpin = None

    def _is_deinited(self):
        if self._pwmpin is None:
            raise ValueError(
                "Object has been deinitialize and can no longer "
                "be used. Create a new object."
            )

    def _write_pin_attr(self, attr, value):
        # Make sure the pin is active
        self._is_deinited()

        path = os.path.join(
            self._sysfs_path,
            self._channel_path.format(self._channel),
            self._pin_path.format(self._pwmpin),
            attr,
        )

        with open(path, "w", encoding="utf-8") as f_attr:
            # print(value, path)
            f_attr.write(value + "\n")

    def _read_pin_attr(self, attr):
        # Make sure the pin is active
        self._is_deinited()

        path = os.path.join(
            self._sysfs_path,
            self._channel_path.format(self._channel),
            self._pin_path.format(self._pwmpin),
            attr,
        )

        with open(path, "r", encoding="utf-8") as f_attr:
            return f_attr.read().strip()

    # Mutable properties

    def _get_period(self):
        period_ns = self._read_pin_attr(self._pin_period_path)
        try:
            period_ns = int(period_ns)
        except ValueError:
            raise PWMError(
                None, 'Unknown period value: "%s"' % period_ns
            ) from ValueError

        # Convert period from nanoseconds to seconds
        period = period_ns / 1e9

        # Update our cached period
        self._period = period

        return period

    def _set_period(self, period):
        if not isinstance(period, (int, float)):
            raise TypeError("Invalid period type, should be int or float.")

        # Convert period from seconds to integer nanoseconds
        period_ns = int(period * 1e9)

        self._write_pin_attr(self._pin_period_path, "{}".format(period_ns))

        # Update our cached period
        self._period = float(period)

    period = property(_get_period, _set_period)

    """Get or set the PWM's output period in seconds.

    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int or float.

    :type: int, float
    """

    def _get_duty_cycle(self):
        duty_cycle_ns = self._read_pin_attr(self._pin_duty_cycle_path)
        try:
            duty_cycle_ns = int(duty_cycle_ns)
        except ValueError:
            raise PWMError(
                None, 'Unknown duty cycle value: "%s"' % duty_cycle_ns
            ) from ValueError

        # Convert duty cycle from nanoseconds to seconds
        duty_cycle = duty_cycle_ns / 1e9

        # Convert duty cycle to ratio from 0.0 to 1.0
        duty_cycle = duty_cycle / self._period

        # convert to 16-bit
        duty_cycle = int(duty_cycle * 65535)
        return duty_cycle

    def _set_duty_cycle(self, duty_cycle):
        if not isinstance(duty_cycle, (int, float)):
            raise TypeError("Invalid duty cycle type, should be int or float.")

        # convert from 16-bit
        duty_cycle /= 65535.0
        if not 0.0 <= duty_cycle <= 1.0:
            raise ValueError("Invalid duty cycle value, should be between 0.0 and 1.0.")

        # Convert duty cycle from ratio to seconds
        duty_cycle = duty_cycle * self._period

        # Convert duty cycle from seconds to integer nanoseconds
        duty_cycle_ns = int(duty_cycle * 1e9)

        self._write_pin_attr(self._pin_duty_cycle_path, "{}".format(duty_cycle_ns))

    duty_cycle = property(_get_duty_cycle, _set_duty_cycle)
    """Get or set the PWM's output duty cycle as a ratio from 0.0 to 1.0.

    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int or float.
        ValueError: if value is out of bounds of 0.0 to 1.0.

    :type: int, float
    """

    def _get_frequency(self):
        return 1.0 / self._get_period()

    def _set_frequency(self, frequency):
        if not isinstance(frequency, (int, float)):
            raise TypeError("Invalid frequency type, should be int or float.")

        self._set_period(1.0 / frequency)

    frequency = property(_get_frequency, _set_frequency)
    """Get or set the PWM's output frequency in Hertz.

    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int or float.

    :type: int, float
    """

    def _get_enabled(self):
        enabled = self._read_pin_attr(self._pin_enable_path)

        if enabled == "1":
            return True
        if enabled == "0":
            return False

        raise PWMError(None, 'Unknown enabled value: "%s"' % enabled)

    def _set_enabled(self, value):
        """Get or set the PWM's output enabled state.

        Raises:
            PWMError: if an I/O or OS error occurs.
            TypeError: if value type is not bool.

        :type: bool
        """
        if not isinstance(value, bool):
            raise TypeError("Invalid enabled type, should be string.")

        self._write_pin_attr(self._pin_enable_path, "1" if value else "0")

    # String representation

    def __str__(self):
        return "PWM%d, pin %s (freq=%f Hz, duty_cycle=%f%%)" % (
            self._channel,
            self._pin,
            self.frequency,
            self.duty_cycle * 100,
        )
