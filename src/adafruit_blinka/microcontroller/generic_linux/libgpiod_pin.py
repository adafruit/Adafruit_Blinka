# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""A Pin class for use with libgpiod."""
try:
    import gpiod
except ImportError:
    raise ImportError(
        "libgpiod Python bindings not found, please install and try again! See "
        "https://github.com/adafruit/Raspberry-Pi-Installer-Scripts/blob/main/libgpiod.py"
    ) from ImportError

# Versions 1.5.4 and earlier have no __version__ attribute
if hasattr(gpiod, "__version__"):
    version = gpiod.__version__
else:
    version = "1.x"

if version.startswith("1."):
    from .libgpiod.libgpiod_pin_1_x import Pin  # pylint: disable=unused-import
else:
    from .libgpiod.libgpiod_pin_2_x import Pin  # pylint: disable=unused-import
