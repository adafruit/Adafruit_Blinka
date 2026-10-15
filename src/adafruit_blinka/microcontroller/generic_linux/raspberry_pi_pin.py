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


def _close_chip(chip):
    if hasattr(chip, "close"):
        chip.close()
    else:
        chip.reset()


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
        except BaseException:
            try:
                _close_chip(chip)
            except BaseException:
                pass  # Preserve the metadata error if cleanup also fails.
            raise
        _close_chip(chip)
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

    def __init__(self, bcm_number):
        self._chip_index = None
        if isinstance(bcm_number, bool):
            raise TypeError("BCM GPIO number must be an integer")
        try:
            offset = operator.index(bcm_number)
        except TypeError:
            raise TypeError("BCM GPIO number must be an integer") from None
        if offset < 0:
            raise ValueError("BCM GPIO number must be nonnegative")
        super().__init__(offset)

    @property
    def chip_index(self):
        """Header controller index, without retaining a discovery handle."""
        return self._chip_index if self._chip is not None else _find_chip(self.id)

    def _open_chip(self):
        index = _find_chip(self.id)
        chip = _open_chip(index)
        try:
            label, count = _chip_info(chip)
            if label not in _LABELS or self.id >= count:
                raise RuntimeError("Raspberry Pi header GPIO controller changed")
        except BaseException:
            try:
                _close_chip(chip)
            except BaseException:
                pass
            raise
        self._chip_index = index
        return chip
