# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`analogio` - Analog input control
=================================================
Read the SysFS ADC using IIO (Industrial Input/Output) and return the value

See `CircuitPython:analogio` in CircuitPython for more details.
* Author(s): Melissa LeBlanc-Williams
"""

import os
from adafruit_blinka import ContextManaged

try:
    from microcontroller.pin import analogIns
except ImportError:
    raise RuntimeError("No Analog Inputs defined for this board") from ImportError


class AnalogIn(ContextManaged):
    """Analog Input Class"""

    # Sysfs paths
    _sysfs_path = "/sys/bus/iio/devices/"
    _device_path = "iio:device{}"

    # Channel paths
    _channel_path = "in_voltage{}_raw"
    _scale_path = "in_voltage_scale"

    def __init__(self, adc_id):
        """Instantiate an AnalogIn object and verify the sysfs IIO
        corresponding to the specified channel and pin.

        Args:
            adc_id (int): Analog Input ID as defined in microcontroller.pin

        Returns:
            AnalogIn: AnalogIn object.

        Raises:
            TypeError: if `channel` or `pin` types are invalid.
            ValueError: if AnalogIn channel does not exist.

        """

        self.id = adc_id
        self._device = None
        self._channel = None
        self._open(adc_id)

    def __enter__(self):
        return self

    def _open(self, adc_id):
        self._device = None
        for adcpair in analogIns:
            if adcpair[0] == adc_id:
                self._device = adcpair[1]
                self._channel = adcpair[2]

        if self._device is None:
            raise RuntimeError("No AnalogIn device found for the given ID")

        device_path = os.path.join(
            self._sysfs_path, self._device_path.format(self._device)
        )

        if not os.path.isdir(device_path):
            raise ValueError(
                "AnalogIn device does not exist, check that the required modules are loaded."
            )

    @property
    def value(self):
        """Read the ADC and return the value as an integer"""
        path = os.path.join(
            self._sysfs_path,
            self._device_path.format(self._device),
            self._channel_path.format(self._channel),
        )

        with open(path, "r", encoding="utf-8") as analog_in:
            return int(analog_in.read().strip())

    # pylint: disable=no-self-use
    @value.setter
    def value(self, value):
        # emulate what CircuitPython does
        raise AttributeError("'AnalogIn' object has no attribute 'value'")

    # pylint: enable=no-self-use

    def deinit(self):
        self._device = None
        self._channel = None
