
try:
    from microcontroller.pin import pwmOuts
except ImportError:
    raise RuntimeError("No PWM outputs defined for this board")

from microcontroller.pin import Pin

class PWMError(IOError):
    """Base class for PWM errors."""
    pass


class PWMOut(object):
    # Nova instance
    _nova = None
    MAX_CYCLE_LEVEL = 1024

    def __init__(self, pin, *, frequency=750, duty_cycle=0, variable_frequency=False):
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
        if PWMOut._nova is None:
            from adafruit_blinka.microcontroller.nova import Connection
            PWMOut._nova = Connection.getInstance()

        PWMOut._nova.setOperationMode(0, 'IO')
        self._pwmpin = None
        self._open(pin, duty_cycle, frequency, variable_frequency)

    def __del__(self):
        self.deinit()

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self.deinit()

    def _open(self, pin, duty=0, freq=750, variable_frequency=False):
        self._channel = None
        for pwmpair in pwmOuts:
            if pwmpair[1] == pin:
                self._channel = pwmpair[0][0]
                self._pwmpin = pwmpair[0][1]

        self._pin = pin
        if self._channel is None:
            raise RuntimeError("No PWM channel found for this Pin")

        PWMOut._nova.setIOpinMode(self._pwmpin, Pin.PWM)

        # set frequency
        self.frequency = freq
        # set period
        self._period = self._get_period()

        # set duty
        self.duty_cycle = duty

        self._set_enabled(True)

    def deinit(self):
        try:
            """Deinit the Nova PWM."""
            if self._channel is not None:
                #self.duty_cycle = 0
                self._set_enabled(False) # make to disable before unexport

        except Exception as e:
            # due to a race condition for which I have not yet been
            # able to find the root cause, deinit() often fails
            # but it does not effect future usage of the pwm pin
            print("warning: failed to deinitialize pwm pin {0}:{1} due to: {2}\n".format(self._channel, self._pwmpin, type(e).__name__))
        finally:
            self._channel = None
            self._pwmpin = None

    def _is_deinited(self):
        if self._pwmpin is None:
            raise ValueError("Object has been deinitialize and can no longer "
                             "be used. Create a new object.")

    # Mutable properties

    def _get_period(self):
        return 1.0 / self._get_frequency()

    def _set_period(self, period):
        if not isinstance(period, (int, float)):
            raise TypeError("Invalid period type, should be int or float.")

        self._set_frequency(1.0 / period)

    period = property(_get_period, _set_period)

    """Get or set the PWM's output period in seconds.

    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int or float.

    :type: int, float
    """

    def _get_duty_cycle(self):
        duty_cycle = Pin._nova.getIOpinValue(self._pwmpin)

        # Convert duty cycle to ratio from 0.0 to 1.0
        duty_cycle = duty_cycle / PWMOut.MAX_CYCLE_LEVEL

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

        # Convert duty cycle from ratio to 1024 levels
        duty_cycle = duty_cycle * PWMOut.MAX_CYCLE_LEVEL

        # Set duty cycle
        Pin._nova.setIOpinValue(self._pwmpin, duty_cycle)

    duty_cycle = property(_get_duty_cycle, _set_duty_cycle)
    """Get or set the PWM's output duty cycle as a ratio from 0.0 to 1.0.

    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int or float.
        ValueError: if value is out of bounds of 0.0 to 1.0.

    :type: int, float
    """

    def _get_frequency(self):
        return int(PWMOut._nova.getIOpinPWMFreq(self._pwmpin).split('PWMFREQ ')[1])

    def _set_frequency(self, frequency):
        if not isinstance(frequency, (int, float)):
            raise TypeError("Invalid frequency type, should be int or float.")

        PWMOut._nova.setIOpinPWMFreq(self._pwmpin, frequency)

    frequency = property(_get_frequency, _set_frequency)
    """Get or set the PWM's output frequency in Hertz.

    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not int or float.

    :type: int, float
    """

    def _get_enabled(self):
        enabled = self._enable

        if enabled == "1":
            return True
        elif enabled == "0":
            return False

        raise PWMError(None, "Unknown enabled value: \"%s\"" % enabled)

    def _set_enabled(self, value):
        if not isinstance(value, bool):
            raise TypeError("Invalid enabled type, should be string.")
        self._enable = value
        if not self._enable:
            self._set_duty_cycle(0.0)
    """Get or set the PWM's output enabled state.

    Raises:
        PWMError: if an I/O or OS error occurs.
        TypeError: if value type is not bool.

    :type: bool
    """

    # String representation

    def __str__(self):
        return "PWM%d, pin %s (freq=%f Hz, duty_cycle=%f%%)" % \
            (self._pin, self._pin, self.frequency, self.duty_cycle * 100,)
