# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`analogio` - Analog output control
=================================================
Write the SysFS DAC using IIO (Industrial Input/Output)

See `CircuitPython:analogio` in CircuitPython for more details.
* Author(s): Melissa LeBlanc-Williams
"""

import os
from adafruit_blinka import ContextManaged

try:
    from microcontroller.pin import analogOuts
except ImportError:
    raise RuntimeError("No Analog Outputs defined for this board") from ImportError


class AnalogOut(ContextManaged):
    """Analog Output Class"""

    # Sysfs paths
    _sysfs_path = "/sys/bus/iio/devices/"
    _device_path = "iio:device{}"

    # Channel paths
    _channel_path = "out_voltage{}_raw"
    _scale_path = "out_voltage_scale"

    def __init__(self, dac_id):
        """Instantiate an AnalogOut object and verify the sysfs IIO
        corresponding to the specified channel and pin.

        Args:
            dac_id (int): Analog Output ID as defined in microcontroller.pin

        Returns:
            AnalogOut: AnalogOut object.

        Raises:
            TypeError: if `channel` or `pin` types are invalid.
            ValueError: if AnalogOut channel does not exist.

        """

        self.id = dac_id
        self._device = None
        self._channel = None
        self._open(dac_id)

    def __enter__(self):
        return self

    def _open(self, dac_id):
        self._device = None
        for dacpair in analogOuts:
            if dacpair[0] == dac_id:
                self._device = dacpair[1]
                self._channel = dacpair[2]

        if self._device is None:
            raise RuntimeError("No AnalogOut device found for the given ID")

        device_path = os.path.join(
            self._sysfs_path, self._device_path.format(self._device)
        )

        if not os.path.isdir(device_path):
            raise ValueError(
                "AnalogOut device does not exist, check that the required modules are loaded."
            )

    @property
    def value(self):
        """Return an error. This is output only."""
        # emulate what CircuitPython does
        raise AttributeError("unreadable attribute")

    @value.setter
    def value(self, value):
        """Write to the DAC"""
        path = os.path.join(
            self._sysfs_path,
            self._device_path.format(self._device),
            self._channel_path.format(self._channel),
        )

        with open(path, "w", encoding="utf-8") as analog_out:
            return analog_out.write(value + "\n")

    def deinit(self):
        self._device = None
        self._channel = None
