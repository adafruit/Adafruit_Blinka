"""PWMOut Class for RP2040s with u2if"""
from .rp2040_u2if import rp2040_u2if


class PWMOut:
    """Base Pulse Width Modulation Output Class"""

    def __init__(self, pin, *, frequency=500, duty_cycle=0, variable_frequency=False):
        rp2040_u2if.pwm_configure(
            pin,
            frequency=frequency,
            duty_cycle=duty_cycle,
            variable_frequency=variable_frequency,
        )

        self._pin = pin

    def __del__(self):
        self.deinit()

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self.deinit()

    def deinit(self):
        """Deinit PWM."""
        rp2040_u2if.pwm_deinit(self._pin)

    @property
    def duty_cycle(self):
        """The PWM's output duty cycle, 16-bit."""
        return rp2040_u2if.pwm_get_duty_cycle(self._pin)

    @duty_cycle.setter
    def duty_cycle(self, duty_cycle):
        rp2040_u2if.pwm_set_duty_cycle(self._pin, duty_cycle)

    @property
    def frequency(self):
        """The PWM's output frequency in Hertz."""
        return rp2040_u2if.pwm_get_frequency(self._pin)

    @frequency.setter
    def frequency(self, frequency):
        rp2040_u2if.pwm_set_frequency(self._pin, frequency)
