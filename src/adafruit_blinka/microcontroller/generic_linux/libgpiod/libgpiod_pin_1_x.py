# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""A Pin class for use with libgpiod 1.x."""
import errno

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
        self._chip = self._line = None
        self.id = pin_id
        self._mode, self._value = self.IN, self.LOW
        self._num = int(pin_id[1] if isinstance(pin_id, tuple) else pin_id)

    def _open_chip(self):
        """Open this pin's controller; subclasses may discover its identity."""
        chip_class = gpiod.Chip if hasattr(gpiod, "Chip") else gpiod.chip
        if isinstance(self.id, tuple):
            return chip_class(str(self.id[0]), chip_class.OPEN_BY_NUMBER)
        return chip_class("gpiochip0", chip_class.OPEN_BY_NAME)

    def _ensure_chip(self):
        if self._chip is None:
            self._chip = self._open_chip()

    def _bias_flags(self, pull):
        implicit = pull is None
        if implicit:
            pull = self.PULL_NONE
        names = {
            self.PULL_NONE: "BIAS_DISABLE",
            self.PULL_UP: "BIAS_PULL_UP",
            self.PULL_DOWN: "BIAS_PULL_DOWN",
        }
        if pull not in names:
            raise RuntimeError(f"Invalid pull for pin: {self.id}")
        if hasattr(gpiod, "LINE_REQ_DIR_IN"):
            flag = getattr(gpiod, "LINE_REQ_FLAG_" + names[pull], None)
        else:
            flag = getattr(gpiod.line_request, "FLAG_" + names[pull], None)
        if flag is None:
            # Early bindings cannot explicitly disable bias. Preserve their
            # normal input initialization, but never silently accept an
            # explicit request for a pull setting that cannot be supplied.
            if implicit:
                return 0
            if pull == self.PULL_NONE:
                raise NotImplementedError(
                    "This libgpiod backend cannot explicitly disable pin bias"
                )
            raise NotImplementedError(
                "Requested pull setting not supported in libgpiod"
            )
        return flag

    def __del__(self):
        self.deinit()

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def _request_line(self, mode, flags):
        """Request one line using the installed 1.x binding's API."""
        if hasattr(gpiod, "LINE_REQ_DIR_IN"):
            arguments = {
                "consumer": self._CONSUMER,
                "type": gpiod.LINE_REQ_DIR_IN
                if mode == self.IN
                else gpiod.LINE_REQ_DIR_OUT,
                "flags": flags,
            }
            if mode == self.OUT:
                arguments["default_vals"] = [int(self._value)]
            self._line.request(**arguments)
        else:
            config = gpiod.line_request()
            config.consumer = self._CONSUMER
            config.request_type = (
                gpiod.line_request.DIRECTION_INPUT
                if mode == self.IN
                else gpiod.line_request.DIRECTION_OUTPUT
            )
            config.flags = flags
            if mode == self.OUT:
                self._line.request(config, default_val=int(self._value))
            else:
                self._line.request(config)

    def init(self, mode=IN, pull=None):
        """Initialize or reconfigure this pin, opening its controller on demand."""
        try:
            if mode is None and pull is not None:
                mode = self._mode
            if mode == self.OUT and pull is not None:
                raise RuntimeError("Cannot set pull resistor on output")
            if mode is not None and mode not in (self.IN, self.OUT):
                raise RuntimeError(f"Invalid mode for pin: {self.id}")
            flags = self._bias_flags(pull) if mode is not None else 0
            self._ensure_chip()
            if self._line is None:
                self._line = self._chip.get_line(int(self._num))
            if mode is not None:
                self._line.release()
                try:
                    self._request_line(mode, flags)
                except OSError as error:
                    # Linux before 5.5 rejects the bias flags even when the
                    # bindings expose them. Preserve implicit no-pull setup on
                    # those kernels, but do not relax explicit pull requests.
                    if pull is not None or not flags or error.errno != errno.EINVAL:
                        raise
                    self._request_line(mode, 0)
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
        # Keep failed handles reachable so callers can retry cleanup. A line
        # still awaiting release also needs its owning chip to remain open.
        if getattr(self, "_line", None) is not None:
            self._line.release()
            self._line = None
        if getattr(self, "_chip", None) is not None:
            if hasattr(self._chip, "close"):
                self._chip.close()
            else:
                self._chip.reset()
            self._chip = None

    def value(self, val=None):
        """Set or return the Pin Value"""
        if val is None:
            return self._line.get_value()

        if val in (self.LOW, self.HIGH):
            self._line.set_value(val)
            self._value = val
            return None
        raise RuntimeError("Invalid value for pin")
