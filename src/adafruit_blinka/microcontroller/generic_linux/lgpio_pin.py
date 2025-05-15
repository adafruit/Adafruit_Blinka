# SPDX-FileCopyrightText: 2025 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""A Pin class for use with lgpio."""

from pathlib import Path
import lgpio


def _get_gpiochip():
    """
    Determines the handle of the GPIO chip device to access.

    iterate through sysfs  to find a GPIO chip device with a driver known to be
    used for userspace GPIO access.
    """
    for dev in Path("/sys/bus/gpio/devices").glob("gpiochip*"):
        if Path(dev / "of_node/compatible").is_file():
            drivers = set((dev / "of_node/compatible").read_text().split("\0"))
            #   check if driver names are intended for userspace control
            if drivers & {
                "raspberrypi,rp1-gpio",
                "raspberrypi,bcm2835-gpio",
                "raspberrypi,bcm2711-gpio",
            }:
                return lgpio.gpiochip_open(int(dev.name[-1]))
    # return chip0 as a fallback
    return lgpio.gpiochip_open(0)


CHIP = _get_gpiochip()


class Pin:
    """Pins dont exist in CPython so...lets make our own!"""

    LOW = 0
    HIGH = 1
    OFF = LOW
    ON = HIGH

    # values of lg mode constants
    PULL_NONE = 0x80
    PULL_UP = 0x20
    PULL_DOWN = 0x40
    ACTIVE_LOW = 0x02

    # drive mode lg constants
    OPEN_DRAIN = 0x04
    IN = 0x0100
    OUT = 0x0200

    # LG mode constants
    _LG_ALERT = 0x400
    _LG_GROUP = 0x800
    _LG_MODES = IN | OUT | _LG_ALERT | _LG_GROUP
    _LG_PULLS = PULL_NONE | PULL_UP | PULL_NONE | ACTIVE_LOW
    _LG_DRIVES = OPEN_DRAIN

    id = None
    _value = LOW
    _mode = IN

    # we want exceptions
    lgpio.exceptions = True

    def __init__(self, bcm_number):
        self.id = bcm_number

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        if mode is not None:
            if mode == Pin.IN:
                self._mode = Pin.IN
                self._set_gpio_mode_in()
            elif mode == self.OUT:
                self._mode = Pin.OUT
                Pin._check_result(lgpio.gpio_claim_output(CHIP, self.id, Pin.LOW))
            else:
                raise RuntimeError(f"Invalid mode for pin: {self.id}")
        if pull is not None:
            if self._mode != Pin.IN:
                raise RuntimeError("Can only set pull resistor on input")
            if pull in {Pin.PULL_UP, Pin.PULL_DOWN, Pin.PULL_NONE}:
                self._set_gpio_mode_in(lflags=pull)
            else:
                raise RuntimeError(f"Invalid pull for pin: {self.id}")

    def value(self, val=None):
        """Set or return the Pin Value"""
        if val is not None:
            if val == Pin.LOW:
                self._value = val
                Pin._check_result(lgpio.gpio_write(CHIP, self.id, val))
            elif val == Pin.HIGH:
                self._value = val
                Pin._check_result(lgpio.gpio_write(CHIP, self.id, val))
            else:
                raise RuntimeError("Invalid value for pin")
            return None
        return Pin._check_result(lgpio.gpio_read(CHIP, self.id))

    @staticmethod
    def _check_result(result):
        """
        convert any result other than zero to a text message and pass it back
        as a runtime exception.  Typical usage:  use the lgpio call as the
        argument.
        """
        if result < 0:
            raise RuntimeError(lgpio.error_text(result))
        return result

    def _set_gpio_mode_in(self, lflags=0):
        """
        claim a gpio as input, or modify the flags (PULL_UP, PULL_DOWN, ... )
        """
        # This gpio_free may seem redundant, but is required when
        #  changing the line-flags of an already acquired input line
        try:
            lgpio.gpio_free(CHIP, self.id)
        except lgpio.error:
            pass
        Pin._check_result(lgpio.gpio_claim_input(CHIP, self.id, lFlags=lflags))
