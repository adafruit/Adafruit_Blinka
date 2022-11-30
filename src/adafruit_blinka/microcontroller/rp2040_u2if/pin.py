# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Generic RP2040 pin names"""
from .rp2040_u2if import rp2040_u2if


class Pin:
    """A basic Pin class for use with RP2040 with u2if firmware."""

    # pin modes
    IN = 0
    OUT = 1
    # pin values
    LOW = 0
    HIGH = 1
    # pin pulls
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2

    def __init__(self, pin_id=None):
        self.id = pin_id
        self._mode = None
        self._pull = None

    # pylint:disable = no-self-use
    def _u2if_open_hid(self, vid, pid):
        rp2040_u2if.open(vid, pid)

    def init(self, mode=IN, pull=PULL_NONE):
        """Initialize the Pin"""
        pull = Pin.PULL_NONE if pull is None else pull
        if self.id is None:
            raise RuntimeError("Can not init a None type pin.")
        if mode not in (Pin.IN, Pin.OUT):
            raise ValueError("Incorrect mode value.")
        if pull not in (Pin.PULL_NONE, Pin.PULL_UP, Pin.PULL_DOWN):
            raise ValueError("Incorrect pull value.")

        rp2040_u2if.gpio_init_pin(self.id, mode, pull)

        self._mode = mode
        self._pull = pull

    def value(self, val=None):
        """Set or return the Pin Value"""
        # Digital In / Out
        if self._mode in (Pin.IN, Pin.OUT):
            # digital read
            if val is None:
                return rp2040_u2if.gpio_get_pin(self.id)
            # digital write
            if val in (Pin.LOW, Pin.HIGH):
                rp2040_u2if.gpio_set_pin(self.id, val)
                return None
            # nope
            raise ValueError("Invalid value for pin.")

        raise RuntimeError(
            "No action for mode {} with value {}".format(self._mode, val)
        )


# create pin instances for each pin
GP0 = Pin(0)
GP1 = Pin(1)
GP2 = Pin(2)
GP3 = Pin(3)
GP4 = Pin(4)
GP5 = Pin(5)
GP6 = Pin(6)
GP7 = Pin(7)
GP8 = Pin(8)
GP9 = Pin(9)
GP10 = Pin(10)
GP11 = Pin(11)
GP12 = Pin(12)
GP13 = Pin(13)
GP14 = Pin(14)
GP15 = Pin(15)
GP16 = Pin(16)
GP17 = Pin(17)
GP18 = Pin(18)
GP19 = Pin(19)
GP20 = Pin(20)
GP21 = Pin(21)
GP22 = Pin(22)
GP23 = Pin(23)
GP24 = Pin(24)
GP25 = Pin(25)
GP26 = Pin(26)
GP27 = Pin(27)
GP28 = Pin(28)
GP29 = Pin(29)
