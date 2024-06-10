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
    raise RuntimeError("No PWM outputs defined for this board.") from ImportError


# pylint: disable=unnecessary-pass, too-many-instance-attributes


class PWMError(IOError):
    """Base class for PWM errors."""

    pass


# pylint: enable=unnecessary-pass


class PWMOut:
    """Pulse Width Modulation Output Class"""

    # Number of retries to check for successful PWM export on open
    PWM_STAT_RETRIES = 10
    # Delay between check for successful PWM export on open (100ms)
    PWM_STAT_DELAY = 0.1

    # Sysfs paths
    _chip_path = "pwmchip{}"
    _channel_path = "pwm{}"

    def __init__(self, pwm, *, frequency=500, duty_cycle=0, variable_frequency=False):
        """Instantiate a PWM object and open the sysfs PWM corresponding to the
        specified chip and channel.
        Args:
            pwm (str): PWM pin.
            frequency (int, float): target frequency in Hertz (32-bit).
            duty_cycle (int, float): The fraction of each pulse which is high (16-bit).
            variable_frequency (bool): True if the frequency will change over time.
        Returns:
            PWM: PWM object.
        Raises:
            PWMError: if an I/O or OS error occurs.
            TypeError: if `chip` or `channel` types are invalid.
            LookupError: if PWM chip does not exist.
            TimeoutError: if waiting for PWM export times out.
        """

        self._chip = None
        self._channel = None
        self._period_ns = 0
        self._open(pwm, frequency, duty_cycle, variable_frequency)

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _open(self, pwm, frequency, duty_cycle, variable_frequency):
        for pwmout in pwmOuts:
            if pwmout[1] == pwm:
                self._chip = pwmout[0][0]
                self._channel = pwmout[0][1]

        self._chip_path = os.path.join(
            "/sys/class/pwm", self._chip_path.format(self._chip)
        )
        self._channel_path = os.path.join(
            self._chip_path, self._channel_path.format(self._channel)
        )

        if variable_frequency:
            print("Variable Frequency is not supported, continuing without it...")

        if not os.path.isdir(self._chip_path):
            raise LookupError("Opening PWM: PWM chip {} not found.".format(self._chip))

        if not os.path.isdir(self._channel_path):
            # Exporting the PWM.
            try:
                with open(
                    os.path.join(self._chip_path, "export"), "w", encoding="utf-8"
                ) as f_export:
                    f_export.write("{:d}\n".format(self._channel))
            except IOError as e:
                raise PWMError(
                    e.errno, "Exporting PWM channel: " + e.strerror
                ) from IOError

            # Loop until PWM is exported
            exported = False
            for i in range(PWMOut.PWM_STAT_RETRIES):
                if os.path.isdir(self._channel_path):
                    exported = True
                    break

                sleep(PWMOut.PWM_STAT_DELAY)

            if not exported:
                raise TimeoutError(
                    'Exporting PWM: waiting for "{:s}" timed out.'.format(
                        self._channel_path
                    )
                )

            # Loop until 'period' is writable, This could take some time after
            # export as application of the udev rules after export is asynchronous.
            # Without this loop, the following properties may not be writable yet.
            for i in range(PWMOut.PWM_STAT_RETRIES):
                try:
                    with open(
                        os.path.join(self._channel_path, "period"),
                        "w",
                        encoding="utf-8",
                    ):
                        break
                except IOError as e:
                    if e.errno != EACCES or (
                        e.errno == EACCES and i == PWMOut.PWM_STAT_RETRIES - 1
                    ):
                        raise PWMError(
                            e.errno, "Opening PWM period: " + e.strerror
                        ) from IOError

                sleep(PWMOut.PWM_STAT_DELAY)

            self.frequency = frequency
            self.duty_cycle = duty_cycle
            self.polarity = "normal"
            self.enable()

            # Cache the period for fast duty cycle updates
            self._period_ns = self._get_period_ns()

    def close(self):
        """Close the PWM."""
        if self._channel is not None:
            # Unexporting the PWM channel
            try:
                unexport_fd = os.open(
                    os.path.join(self._chip_path, "unexport"), os.O_WRONLY
                )
                os.write(unexport_fd, "{:d}\n".format(self._channel).encode())
                os.close(unexport_fd)
            except OSError as e:
                raise PWMError(e.errno, "Unexporting PWM: " + e.strerror) from OSError

        self._chip = None
        self._channel = None

    def _write_channel_attr(self, attr, value):
        with open(
            os.path.join(self._channel_path, attr), "w", encoding="utf-8"
        ) as f_attr:
            f_attr.write(value + "\n")

    def _read_channel_attr(self, attr):
        with open(
            os.path.join(self._channel_path, attr), "r", encoding="utf-8"
        ) as f_attr:
            return f_attr.read().strip()

    # Methods

    def enable(self):
        """Enable the PWM output."""
        self.enabled = True

    def disable(self):
        """Disable the PWM output."""
        self.enabled = False

    # Mutable properties

    def _get_period(self):
        return float(self.period_ms) / 1000

    def _set_period(self, period):
        if not isinstance(period, (int, float)):
            raise TypeError("Invalid period type, should be int.")

        self.period_ms = int(period * 1000)

    period = property(_get_period, _set_period)
    """Get or set the PWM's output period in seconds.

    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int.

    :type: int, float
    """

    def _get_period_ms(self):
        return self.period_us / 1000

    def _set_period_ms(self, period_ms):
        if not isinstance(period_ms, (int, float)):
            raise TypeError("Invalid period type, should be int or float.")
        self.period_us = int(period_ms * 1000)

    period_ms = property(_get_period_ms, _set_period_ms)
    """Get or set the PWM's output period in milliseconds.

    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int.

    :type: int, float
    """

    def _get_period_us(self):
        return self.period_ns / 1000

    def _set_period_us(self, period_us):
        if not isinstance(period_us, int):
            raise TypeError("Invalid period type, should be int.")

        self.period_ns = int(period_us * 1000)

    period_us = property(_get_period_us, _set_period_us)
    """Get or set the PWM's output period in microseconds.

    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int.

    :type: int
    """

    def _get_period_ns(self):
        period_ns = self._read_channel_attr("period")
        try:
            period_ns = int(period_ns)
        except ValueError:
            raise PWMError(
                None, 'Unknown period value: "%s".' % period_ns
            ) from ValueError

        self._period_ns = period_ns

        return period_ns

    def _set_period_ns(self, period_ns):
        if not isinstance(period_ns, int):
            raise TypeError("Invalid period type, should be int.")

        self._write_channel_attr("period", str(period_ns))

        # Update our cached period
        self._period_ns = period_ns

    period_ns = property(_get_period_ns, _set_period_ns)
    """Get or set the PWM's output period in nanoseconds.

    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int.

    :type: int
    """

    def _get_duty_cycle_ns(self):
        duty_cycle_ns_str = self._read_channel_attr("duty_cycle")

        try:
            duty_cycle_ns = int(duty_cycle_ns_str)
        except ValueError:
            raise PWMError(
                None, 'Unknown duty cycle value: "{:s}"'.format(duty_cycle_ns_str)
            ) from ValueError

        return duty_cycle_ns

    def _set_duty_cycle_ns(self, duty_cycle_ns):
        if not isinstance(duty_cycle_ns, int):
            raise TypeError("Invalid duty cycle type, should be int.")

        self._write_channel_attr("duty_cycle", str(duty_cycle_ns))

    duty_cycle_ns = property(_get_duty_cycle_ns, _set_duty_cycle_ns)
    """Get or set the PWM's output duty cycle in nanoseconds.

    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int.

    :type: int
    """

    def _get_duty_cycle(self):
        return float(self.duty_cycle_ns) / self._period_ns

    def _set_duty_cycle(self, duty_cycle):
        if not isinstance(duty_cycle, (int, float)):
            raise TypeError("Invalid duty cycle type, should be int or float.")

        if not 0.0 <= duty_cycle <= 1.0:
            raise ValueError("Invalid duty cycle value, should be between 0.0 and 1.0.")

        # Convert duty cycle from ratio to nanoseconds
        self.duty_cycle_ns = int(duty_cycle * self._period_ns)

    duty_cycle = property(_get_duty_cycle, _set_duty_cycle)
    """Get or set the PWM's output duty cycle as a ratio from 0.0 to 1.0.
    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int or float.
        ValueError: if value is out of bounds of 0.0 to 1.0.
    :type: int, float
    """

    def _get_frequency(self):
        return 1.0 / self.period

    def _set_frequency(self, frequency):
        if not isinstance(frequency, (int, float)):
            raise TypeError("Invalid frequency type, should be int or float.")

        self.period = 1.0 / frequency

    frequency = property(_get_frequency, _set_frequency)
    """Get or set the PWM's output frequency in Hertz.
    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int or float.
    :type: int, float
    """

    def _get_polarity(self):
        return self._read_channel_attr("polarity")

    def _set_polarity(self, polarity):
        if not isinstance(polarity, str):
            raise TypeError("Invalid polarity type, should be str.")

        if polarity.lower() not in ["normal", "inversed"]:
            raise ValueError('Invalid polarity, can be: "normal" or "inversed".')

        self._write_channel_attr("polarity", polarity.lower())

    polarity = property(_get_polarity, _set_polarity)
    """Get or set the PWM's output polarity. Can be "normal" or "inversed".
    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not str.
        ValueError: if value is invalid.
    :type: str
    """

    def _get_enabled(self):
        enabled = self._read_channel_attr("enable")

        if enabled == "1":
            return True
        if enabled == "0":
            return False

        raise PWMError(None, 'Unknown enabled value: "{:s}"'.format(enabled))

    def _set_enabled(self, value):
        if not isinstance(value, bool):
            raise TypeError("Invalid enabled type, should be bool.")

        self._write_channel_attr("enable", "1" if value else "0")

    enabled = property(_get_enabled, _set_enabled)
    """Get or set the PWM's output enabled state.
    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not bool.
    :type: bool
    """

    # String representation

    def __str__(self):
        return (
            "PWM {:d}, chip {:d} (period={:f} sec, duty_cycle={:f}%,"
            " polarity={:s}, enabled={:s})".format(
                self._channel,
                self._chip,
                self.period,
                self.duty_cycle * 100,
                self.polarity,
                str(self.enabled),
            )
        )
