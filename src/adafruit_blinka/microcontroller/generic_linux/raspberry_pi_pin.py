# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Raspberry Pi BCM-numbered pins backed by the existing libgpiod drivers."""

import operator
import re
from pathlib import Path

import gpiod

from .libgpiod_pin import Pin as _Pin

_LABELS = {"pinctrl-bcm2835", "pinctrl-bcm2711", "pinctrl-rp1"}
_VERSION_1 = getattr(gpiod, "__version__", "1.x").startswith("1.")


def _chip_paths():
    paths = set()
    for path in Path("/dev").glob("gpiochip*"):
        if not re.fullmatch(r"gpiochip[0-9]+", path.name):
            continue
        # Raspberry Pi OS may expose the same device through a compatibility
        # symlink (for example gpiochip4 -> gpiochip0). Inspect it only once.
        canonical = path.resolve()
        if canonical.parent != Path("/dev") or not re.fullmatch(
            r"gpiochip[0-9]+", canonical.name
        ):
            raise RuntimeError("GPIO controller alias must resolve to /dev/gpiochipN")
        paths.add(canonical)
    return sorted(paths)


def _open_chip(index):
    if _VERSION_1:
        chip_class = gpiod.Chip if hasattr(gpiod, "Chip") else gpiod.chip
        return chip_class(str(index), chip_class.OPEN_BY_NUMBER)
    return gpiod.Chip(f"/dev/gpiochip{index}")


def _chip_info(chip):
    if not _VERSION_1:
        info = chip.get_info()
        return info.label, info.num_lines
    label, count = chip.label, chip.num_lines
    return label() if callable(label) else label, count() if callable(count) else count


def _find_chip(offset):
    candidates, inaccessible = [], []
    for path in _chip_paths():
        index = int(path.name[len("gpiochip") :])
        try:
            chip = _open_chip(index)
        except PermissionError as error:
            inaccessible.append(error)
            continue
        try:
            label, count = _chip_info(chip)
            if label in _LABELS and offset < count:
                candidates.append(index)
        finally:
            chip.close()
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1:
        raise RuntimeError(
            "Multiple Raspberry Pi header GPIO controllers match this pin"
        )
    if inaccessible:
        raise PermissionError(
            "Cannot inspect Raspberry Pi GPIO controllers; grant access to the gpio group"
        ) from inaccessible[0]
    raise RuntimeError(f"No Raspberry Pi header GPIO controller exposes GPIO {offset}")


class Pin(_Pin):
    """Keep public BCM integer IDs while owning independent, lazily opened chips."""

    # The base constructor opens hardware; defer it until init() owns a line.
    # pylint: disable=super-init-not-called
    def __init__(self, bcm_number):
        # The base destructors also run after constructor/open failures.
        self._chip = self._line = self._line_request = None
        self._chip_index = None
        if isinstance(bcm_number, bool):
            raise TypeError("BCM GPIO number must be an integer")
        try:
            offset = operator.index(bcm_number)
        except TypeError:
            raise TypeError("BCM GPIO number must be an integer") from None
        if offset < 0:
            raise ValueError("BCM GPIO number must be nonnegative")
        self.id = self._num = offset
        self._mode, self._value = self.IN, self.LOW

    @property
    def chip_index(self):
        """Header controller index, without retaining a discovery handle."""
        return self._chip_index if self._chip is not None else _find_chip(self.id)

    def _ensure_chip(self):
        if self._chip is not None:
            return
        index, offset = _find_chip(self.id), self.id
        try:
            super().__init__((index, offset))
            label, count = _chip_info(self._chip)
            if label not in _LABELS or offset >= count:
                raise RuntimeError("Raspberry Pi header GPIO controller changed")
            self._chip_index = index
        finally:
            self.id = offset

    def init(self, mode=_Pin.IN, pull=None):
        """Configure the pin; reopen its own chip after deinitialization."""
        if mode is None and pull is not None:
            mode = self._mode
        if mode == self.IN and pull is None:
            pull = self.PULL_NONE
        if mode == self.IN and pull == self.PULL_NONE and _VERSION_1:
            # The inherited 1.x implementation requires both of these features.
            if not hasattr(gpiod, "line") or not hasattr(
                gpiod, "LINE_REQ_FLAG_BIAS_DISABLE"
            ):
                raise NotImplementedError(
                    "This libgpiod 1.x backend cannot explicitly disable pin bias"
                )
        try:
            self._ensure_chip()
            if mode == self.OUT and not _VERSION_1:
                if pull is not None:
                    raise RuntimeError("Cannot set pull resistor on output")
                # Reuse the generic request lifecycle, but preserve the commanded
                # output on repeated init (DigitalInOut also configures drive mode).
                super().init(mode=None)
                settings = gpiod.LineSettings()
                settings.direction = gpiod.line.Direction.OUTPUT
                settings.bias = gpiod.line.Bias.DISABLED
                settings.output_value = self._value_map[int(self._value)]
                self._line_request.reconfigure_lines({self._num: settings})
                self._mode = self.OUT
            else:
                super().init(mode=mode, pull=pull)
        except BaseException:
            try:
                self.deinit()
            except BaseException:
                # Keep the original configuration/open error; cleanup was attempted.
                pass
            raise

    def deinit(self):
        """Release only this pin's line/request and chip, including partial setup."""
        line = self._line if _VERSION_1 else self._line_request
        chip = self._chip
        self._chip = self._line = self._line_request = None
        self._chip_index = None
        failure = None
        for handle, operation in ((line, "release"), (chip, "close")):
            if handle is not None:
                try:
                    getattr(handle, operation)()
                except BaseException as error:
                    if failure is None:
                        failure = error
        if failure is not None:
            raise failure
