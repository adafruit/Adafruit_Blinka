# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""A Pin class for use with libgpiod 2.x."""
import gpiod


# pylint: disable=too-many-branches,too-many-statements
class Pin:
    """Pins dont exist in CPython so...lets make our own!"""

    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2
    _CONSUMER = "adafruit_blinka"

    id = None
    _value = LOW
    _mode = IN

    _value_map = (gpiod.line.Value.INACTIVE, gpiod.line.Value.ACTIVE)

    def __init__(self, pin_id):
        self.id = pin_id
        chip_id = 0
        if isinstance(pin_id, tuple):
            chip_id, self._num = pin_id
        if isinstance(chip_id, int):
            chip_id = f"/dev/gpiochip{chip_id}"
        self._chip = gpiod.Chip(chip_id)
        self._line_request = None

    def __del__(self):
        if self._line_request:
            self._line_request.release()

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        # Input,
        if not self._line_request:
            self._line_request = self._chip.request_lines(
                config={int(self._num): None},
                consumer=self._CONSUMER,
            )
            # print("init line: ", self.id, self._line)

        if mode is not None:
            line_config = gpiod.LineSettings()
            if mode == self.IN:
                line_config.direction = gpiod.line.Direction.INPUT
                if pull is not None:
                    if pull == self.PULL_UP:
                        line_config.bias = gpiod.line.Bias.PULL_UP
                    elif pull == self.PULL_DOWN:
                        line_config.bias = gpiod.line.Bias.PULL_DOWN
                    elif pull == self.PULL_NONE:
                        line_config.bias = gpiod.line.Bias.DISABLED
                    else:
                        raise RuntimeError(f"Invalid pull for pin: {self.id}")

                self._mode = self.IN
                self._line_request.reconfigure_lines(
                    {
                        int(self._num): line_config,
                    }
                )
            elif mode == self.OUT:
                if pull is not None:
                    raise RuntimeError("Cannot set pull resistor on output")
                self._mode = self.OUT
                line_config.direction = gpiod.line.Direction.OUTPUT
                self._line_request.reconfigure_lines(
                    {
                        int(self._num): line_config,
                    }
                )
            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)

    def value(self, val=None):
        """Set or return the Pin Value"""
        if val is None:
            return bool(self._value_map.index(self._line_request.get_value(self._num)))

        if val in (self.LOW, self.HIGH):
            self._value = val
            self._line_request.set_value(self._num, self._value_map[int(val)])
            return None
        raise RuntimeError("Invalid value for pin")
