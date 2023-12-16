# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""A Pin class for use with libgpiod 1.x."""
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

    def __init__(self, pin_id):
        self.id = pin_id
        if isinstance(pin_id, tuple):
            self._num = int(pin_id[1])
            if hasattr(gpiod, "Chip"):
                self._chip = gpiod.Chip(str(pin_id[0]), gpiod.Chip.OPEN_BY_NUMBER)
            else:
                self._chip = gpiod.chip(str(pin_id[0]), gpiod.chip.OPEN_BY_NUMBER)
        else:
            self._num = int(pin_id)
            if hasattr(gpiod, "Chip"):
                self._chip = gpiod.Chip("gpiochip0", gpiod.Chip.OPEN_BY_NAME)
            else:
                self._chip = gpiod.chip("gpiochip0", gpiod.chip.OPEN_BY_NAME)
        self._line = None

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        if not self._line:
            self._line = self._chip.get_line(int(self._num))
            # print("init line: ", self.id, self._line)

        if mode is not None:
            if mode == self.IN:
                flags = 0
                self._line.release()
                if pull is not None:
                    if pull == self.PULL_UP:
                        if hasattr(gpiod, "LINE_REQ_FLAG_BIAS_PULL_UP"):
                            flags |= gpiod.LINE_REQ_FLAG_BIAS_PULL_UP
                        else:
                            raise NotImplementedError(
                                "Internal pullups not supported in this version of libgpiod, "
                                "use physical resistor instead!"
                            )
                    elif pull == self.PULL_DOWN:
                        if hasattr(gpiod, "line") and hasattr(
                            gpiod, "LINE_REQ_FLAG_BIAS_PULL_DOWN"
                        ):
                            flags |= gpiod.LINE_REQ_FLAG_BIAS_PULL_DOWN
                        else:
                            raise NotImplementedError(
                                "Internal pulldowns not supported in this version of libgpiod, "
                                "use physical resistor instead!"
                            )
                    elif pull == self.PULL_NONE:
                        if hasattr(gpiod, "line") and hasattr(
                            gpiod, "LINE_REQ_FLAG_BIAS_DISABLE"
                        ):
                            flags |= gpiod.LINE_REQ_FLAG_BIAS_DISABLE
                        else:
                            raise NotImplementedError(
                                "Internal pulldowns not supported in this version of libgpiod, "
                                "use physical resistor instead!"
                            )
                    else:
                        raise RuntimeError(f"Invalid pull for pin: {self.id}")

                self._mode = self.IN
                self._line.release()
                if hasattr(gpiod, "LINE_REQ_DIR_IN"):
                    self._line.request(
                        consumer=self._CONSUMER, type=gpiod.LINE_REQ_DIR_IN, flags=flags
                    )
                else:
                    config = gpiod.line_request()
                    config.consumer = self._CONSUMER
                    config.request_type = gpiod.line_request.DIRECTION_INPUT
                    self._line.request(config)

            elif mode == self.OUT:
                if pull is not None:
                    raise RuntimeError("Cannot set pull resistor on output")
                self._mode = self.OUT
                self._line.release()
                if hasattr(gpiod, "LINE_REQ_DIR_OUT"):
                    self._line.request(
                        consumer=self._CONSUMER, type=gpiod.LINE_REQ_DIR_OUT
                    )
                else:
                    config = gpiod.line_request()
                    config.consumer = self._CONSUMER
                    config.request_type = gpiod.line_request.DIRECTION_OUTPUT
                    self._line.request(config)
            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)

    def value(self, val=None):
        """Set or return the Pin Value"""
        if val is None:
            return self._line.get_value()

        if val in (self.LOW, self.HIGH):
            self._value = val
            self._line.set_value(val)
            return None
        raise RuntimeError("Invalid value for pin")
