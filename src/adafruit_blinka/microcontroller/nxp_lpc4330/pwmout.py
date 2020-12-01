"""PWMOut Class for NXP LPC4330"""

from greatfet import GreatFET

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

    MAX_CYCLE_LEVEL = 1024

    def __init__(self, pin, *, frequency=750, duty_cycle=0, variable_frequency=False):
        """This class makes use of the GreatFET One's Pattern Generator to create a
        Simulated Pulse width modulation. The way that the Pattern Generator works is that
        takes a pattern in the form of bytes and will repeat the output. The trick to simulate
        PWM is to generate the correct byte pattern for the correct channel.

        Args:
            pin (Pin): CircuitPython Pin object to output to
            duty_cycle (int) : The fraction of each pulse which is high. 16-bit
            frequency (int) : target frequency in Hertz (32-bit)

        Returns:
            PWMOut: PWMOut object.

        Raises:
            PWMError: if an I/O or OS error occurs.
            TypeError: if `channel` or `pin` types are invalid.
            ValueError: if PWM channel does not exist.
        """
        self._gf = GreatFET()

        if variable_frequency:
            raise NotImplementedError("Variable Frequency is not currently supported.")

        self._pattern = None
        self._channel = None
        self._enable = False
        self._frequency = 500
        self._duty_cycle = 0
        self._open(pin, duty_cycle, frequency)

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self.deinit()

    def _open(self, pin, duty=0, freq=500):
        self._channel = None
        for pwmpair in pwmOuts:
            if pwmpair[1] == pin:
                self._channel = pwmpair[0]

        self._pin = pin
        if self._channel is None:
            raise RuntimeError("No PWM channel found for this Pin")

        # set duty
        self.duty_cycle = duty

        # set frequency
        self.frequency = freq

        self._set_enabled(True)

    def deinit(self):
        """Deinit the GreatFET One PWM."""
        # pylint: disable=broad-except
        try:
            if self._channel is not None:
                # self.duty_cycle = 0
                self._set_enabled(False)
        except Exception as e:
            # due to a race condition for which I have not yet been
            # able to find the root cause, deinit() often fails
            # but it does not effect future usage of the pwm pin
            print(
                "warning: failed to deinitialize pwm pin {0} due to: {1}\n".format(
                    self._channel, type(e).__name__
                )
            )
        finally:
            self._pattern = None
            self._channel = None
        # pylint: enable=broad-except

    def _is_deinited(self):
        if self._pattern is None:
            raise ValueError(
                "Object has been deinitialize and can no longer "
                "be used. Create a new object."
            )

    # Mutable properties

    def _get_period(self):
        return 1.0 / self._get_frequency()

    def _set_period(self, period):
        """Get or set the PWM's output period in seconds.

        Raises:
            PWMError: if an I/O or OS error occurs.
            TypeError: if value type is not int or float.

        :type: int, float
        """
        if not isinstance(period, (int, float)):
            raise TypeError("Invalid period type, should be int or float.")

        self._set_frequency(1.0 / period)

    period = property(_get_period, _set_period)

    def _get_duty_cycle(self):
        """Get or set the PWM's output duty cycle as a ratio from 0.0 to 1.0.

        Raises:
           PWMError: if an I/O or OS error occurs.
           TypeError: if value type is not int or float.
           ValueError: if value is out of bounds of 0.0 to 1.0.

        :type: int, float
        """
        return self._duty_cycle

    def _set_duty_cycle(self, duty_cycle):
        if not isinstance(duty_cycle, (int, float)):
            raise TypeError("Invalid duty cycle type, should be int or float.")

        # convert from 16-bit
        if isinstance(duty_cycle, int):
            duty_cycle /= 65535.0
        if not 0.0 <= duty_cycle <= 1.0:
            raise ValueError("Invalid duty cycle value, should be between 0.0 and 1.0.")

        # Generate a pattern for 1024 samples of the duty cycle
        pattern = [(1 << self._channel)] * round(PWMOut.MAX_CYCLE_LEVEL * duty_cycle)
        pattern += [(0 << self._channel)] * round(
            PWMOut.MAX_CYCLE_LEVEL * (1.0 - duty_cycle)
        )

        self._pattern = pattern
        self._duty_cycle = duty_cycle
        if self._enable:
            self._set_enabled(True)

    duty_cycle = property(_get_duty_cycle, _set_duty_cycle)

    def _get_frequency(self):
        return self._frequency

    def _set_frequency(self, frequency):
        """Get or set the PWM's output frequency in Hertz.

        Raises:
            PWMError: if an I/O or OS error occurs.
            TypeError: if value type is not int or float.

        :type: int, float
        """
        if not isinstance(frequency, (int, float)):
            raise TypeError("Invalid frequency type, should be int or float.")

        # We are sending 1024 samples per second already
        self._gf.pattern_generator.set_sample_rate(frequency * len(self._pattern))
        self._frequency = frequency

    frequency = property(_get_frequency, _set_frequency)

    def _get_enabled(self):
        enabled = self._enable

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
        self._enable = value
        if self._gf:
            if self._enable:
                if self._pattern:
                    self._gf.pattern_generator.scan_out_pattern(self._pattern)
            else:
                self._gf.pattern_generator.stop()
