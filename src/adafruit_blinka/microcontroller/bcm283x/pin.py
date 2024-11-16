# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Broadcom BCM283x pin names"""
from pathlib import Path
import lgpio


def _get_gpiochip():
    """
    Determines the handle of the GPIO chip device to access.

    iterate through sysfs  to find a GPIO chip device with a driver known to be
    used for userspace GPIO access.
    """
    for dev in Path("/sys/bus/gpio/devices").glob("gpiochip*"):
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
        self.id = bcm_number  # pylint: disable=invalid-name

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


D0 = Pin(0)
D1 = Pin(1)

D2 = Pin(2)
SDA = Pin(2)
D3 = Pin(3)
SCL = Pin(3)

D4 = Pin(4)
D5 = Pin(5)
D6 = Pin(6)

D7 = Pin(7)
CE1 = Pin(7)
D8 = Pin(8)
CE0 = Pin(8)
D9 = Pin(9)
MISO = Pin(9)
D10 = Pin(10)
MOSI = Pin(10)
D11 = Pin(11)
SCLK = Pin(11)  # Raspberry Pi naming
SCK = Pin(11)  # CircuitPython naming

D12 = Pin(12)
D13 = Pin(13)

D14 = Pin(14)
TXD = Pin(14)
D15 = Pin(15)
RXD = Pin(15)

D16 = Pin(16)
D17 = Pin(17)
D18 = Pin(18)
D19 = Pin(19)
MISO_1 = Pin(19)
D20 = Pin(20)
MOSI_1 = Pin(20)
D21 = Pin(21)
SCLK_1 = Pin(21)
SCK_1 = Pin(21)
D22 = Pin(22)
D23 = Pin(23)
D24 = Pin(24)
D25 = Pin(25)
D26 = Pin(26)
D27 = Pin(27)
D28 = Pin(28)
D29 = Pin(29)
D30 = Pin(30)
D31 = Pin(31)
D32 = Pin(32)
D33 = Pin(33)
D34 = Pin(34)
D35 = Pin(35)
D36 = Pin(36)
D37 = Pin(37)
D38 = Pin(38)
D39 = Pin(39)
D40 = Pin(40)
MISO_2 = Pin(40)
D41 = Pin(41)
MOSI_2 = Pin(41)
D42 = Pin(42)
SCLK_2 = Pin(42)
SCK_2 = Pin(43)
D43 = Pin(43)
D44 = Pin(44)
D45 = Pin(45)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SCLK, MOSI, MISO),
    (1, SCLK_1, MOSI_1, MISO_1),
    (2, SCLK_2, MOSI_2, MISO_2),
)

# ordered as uartId, txId, rxId
uartPorts = ((1, TXD, RXD),)

# These are the known hardware I2C ports / pins.
# For software I2C ports created with the i2c-gpio overlay, see:
#     https://github.com/adafruit/Adafruit_Python_Extended_Bus
i2cPorts = (
    (1, SCL, SDA),
    (0, D1, D0),  # both pi 1 and pi 2 i2c ports!
)
