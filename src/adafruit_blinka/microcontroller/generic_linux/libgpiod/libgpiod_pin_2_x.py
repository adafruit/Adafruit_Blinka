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
        self._chip = self._line_request = None
        self.id = pin_id
        self._mode, self._value = self.IN, self.LOW
        chip_id = 0
        if isinstance(pin_id, tuple):
            chip_id, self._num = pin_id
        else:
            self._num = int(pin_id)
        if isinstance(chip_id, int):
            chip_id = f"/dev/gpiochip{chip_id}"
        self._chip_id = chip_id

    def _open_chip(self):
        """Open this pin's controller; subclasses may discover its identity."""
        return gpiod.Chip(self._chip_id)

    def _ensure_chip(self):
        if self._chip is None:
            self._chip = self._open_chip()

    def __del__(self):
        self.deinit()

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        """Initialize or reconfigure this pin, opening its controller on demand."""
        try:
            if mode is None and pull is not None:
                mode = self._mode
            line_config = None
            if mode is not None:
                line_config = gpiod.LineSettings()
                if mode == self.IN:
                    line_config.direction = gpiod.line.Direction.INPUT
                    if pull is None or pull == self.PULL_NONE:
                        line_config.bias = gpiod.line.Bias.DISABLED
                    elif pull == self.PULL_UP:
                        line_config.bias = gpiod.line.Bias.PULL_UP
                    elif pull == self.PULL_DOWN:
                        line_config.bias = gpiod.line.Bias.PULL_DOWN
                    else:
                        raise RuntimeError(f"Invalid pull for pin: {self.id}")
                elif mode == self.OUT:
                    if pull is not None:
                        raise RuntimeError("Cannot set pull resistor on output")
                    line_config.direction = gpiod.line.Direction.OUTPUT
                    line_config.bias = gpiod.line.Bias.DISABLED
                    # DigitalInOut configures OUT again when setting drive_mode.
                    line_config.output_value = self._value_map[int(self._value)]
                else:
                    raise RuntimeError(f"Invalid mode for pin: {self.id}")
            self._ensure_chip()
            if self._line_request is None:
                self._line_request = self._chip.request_lines(
                    config={int(self._num): None}, consumer=self._CONSUMER
                )
            if line_config is not None:
                self._line_request.reconfigure_lines({int(self._num): line_config})
                self._mode = mode
                # Successful input configuration ends the previous output state.
                if mode == self.IN:
                    self._value = self.LOW
        except BaseException:
            try:
                self.deinit()
            except BaseException:
                pass  # Preserve the initialization error if cleanup also fails.
            raise

    def deinit(self):
        """Release the pin and associated resources."""
        request, chip = getattr(self, "_line_request", None), getattr(
            self, "_chip", None
        )
        self._line_request = self._chip = None
        failure = None
        for handle, operation in ((request, "release"), (chip, "close")):
            if handle is not None:
                try:
                    getattr(handle, operation)()
                except BaseException as error:
                    if failure is None:
                        failure = error
        if failure is not None:
            raise failure

    def value(self, val=None):
        """Set or return the Pin Value"""
        if val is None:
            return bool(self._value_map.index(self._line_request.get_value(self._num)))

        if val in (self.LOW, self.HIGH):
            self._line_request.set_value(self._num, self._value_map[int(val)])
            self._value = val
            return None
        raise RuntimeError("Invalid value for pin")
