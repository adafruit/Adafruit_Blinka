"""
Much code from https://github.com/vsergeev/python-periphery/blob/master/periphery/gpio.py
Copyright (c) 2015-2019 vsergeev / Ivan (Vanya) A. Sergeev
License: MIT
"""

import os
import errno
import time

# pylint: disable=unnecessary-pass
class GPIOError(IOError):
    """Base class for GPIO errors."""

    pass


# pylint: enable=unnecessary-pass


class Pin:
    """SysFS GPIO Pin Class"""

    # Number of retries to check for GPIO export or direction write on open
    GPIO_OPEN_RETRIES = 10
    # Delay between check for GPIO export or direction write on open (100ms)
    GPIO_OPEN_DELAY = 0.1

    IN = "in"
    OUT = "out"
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2

    id = None
    _value = LOW
    _mode = IN

    # Sysfs paths
    _sysfs_path = "/sys/class/gpio/"
    _channel_path = "gpiochip{}"

    # Channel paths
    _export_path = "export"
    _unexport_path = "unexport"
    _pin_path = "gpio{}"

    def __init__(self, pin_id):
        """Instantiate a Pin object and open the sysfs GPIO with the specified
        pin number.

        Args:
            pin_id (int): GPIO pin number.

        Returns:
            SysfsGPIO: GPIO object.

        Raises:
            GPIOError: if an I/O or OS error occurs.
            TypeError: if `line` or `direction`  types are invalid.
            ValueError: if `direction` value is invalid.
            TimeoutError: if waiting for GPIO export times out.

        """

        if not isinstance(pin_id, int):
            raise TypeError("Invalid Pin ID, should be integer.")

        self.id = pin_id
        self._fd = None
        self._line = None
        self._path = None

    def __del__(self):
        self._close()

    def __enter__(self):
        return self

    def __exit__(self, t, value, traceback):
        self._close()

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        if mode is not None:
            if mode == self.IN:
                self._mode = self.IN
                self._open(self.IN)
            elif mode == self.OUT:
                self._mode = self.OUT
                self._open(self.OUT)
            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)

            if pull is not None:
                if pull == self.PULL_UP:
                    raise NotImplementedError(
                        "Internal pullups not supported in periphery, "
                        "use physical resistor instead!"
                    )
                if pull == self.PULL_DOWN:
                    raise NotImplementedError(
                        "Internal pulldowns not supported in periphery, "
                        "use physical resistor instead!"
                    )
                raise RuntimeError("Invalid pull for pin: %s" % self.id)

    def value(self, val=None):
        """Set or return the Pin Value"""
        if val is not None:
            if val == self.LOW:
                self._value = val
                self._write(False)
                return None
            if val == self.HIGH:
                self._value = val
                self._write(True)
                return None
            raise RuntimeError("Invalid value for pin")
        return self.HIGH if self._read() else self.LOW

    # pylint: disable=too-many-branches
    def _open(self, direction):
        if not isinstance(direction, str):
            raise TypeError("Invalid direction type, should be string.")
        if direction.lower() not in ["in", "out", "high", "low"]:
            raise ValueError('Invalid direction, can be: "in", "out", "high", "low".')
        gpio_path = "/sys/class/gpio/gpio{:d}".format(self.id)

        if not os.path.isdir(gpio_path):
            # Export the line
            try:
                with open("/sys/class/gpio/export", "w") as f_export:
                    f_export.write("{:d}\n".format(self.id))
            except IOError as e:
                raise GPIOError(e.errno, "Exporting GPIO: " + e.strerror) from IOError

            # Loop until GPIO is exported
            exported = False
            for i in range(self.GPIO_OPEN_RETRIES):
                if os.path.isdir(gpio_path):
                    exported = True
                    break

                time.sleep(self.GPIO_OPEN_DELAY)

            if not exported:
                raise TimeoutError(
                    'Exporting GPIO: waiting for "{:s}" timed out'.format(gpio_path)
                )

            # Write direction, looping in case of EACCES errors due to delayed udev
            # permission rule application after export
            for i in range(self.GPIO_OPEN_RETRIES):
                try:
                    with open(os.path.join(gpio_path, "direction"), "w") as f_direction:
                        f_direction.write(direction.lower() + "\n")
                    break
                except IOError as e:
                    if e.errno != errno.EACCES or (
                        e.errno == errno.EACCES and i == self.GPIO_OPEN_RETRIES - 1
                    ):
                        raise GPIOError(
                            e.errno, "Setting GPIO direction: " + e.strerror
                        ) from IOError

                time.sleep(self.GPIO_OPEN_DELAY)
        else:
            # Write direction
            try:
                with open(os.path.join(gpio_path, "direction"), "w") as f_direction:
                    f_direction.write(direction.lower() + "\n")
            except IOError as e:
                raise GPIOError(
                    e.errno, "Setting GPIO direction: " + e.strerror
                ) from IOError

        # Open value
        try:
            self._fd = os.open(os.path.join(gpio_path, "value"), os.O_RDWR)
        except OSError as e:
            raise GPIOError(e.errno, "Opening GPIO: " + e.strerror) from OSError

        self._path = gpio_path

    # pylint: enable=too-many-branches

    def _close(self):
        if self._fd is None:
            return

        try:
            os.close(self._fd)
        except OSError as e:
            raise GPIOError(e.errno, "Closing GPIO: " + e.strerror) from OSError

        self._fd = None

        # Unexport the line
        try:
            unexport_fd = os.open("/sys/class/gpio/unexport", os.O_WRONLY)
            os.write(unexport_fd, "{:d}\n".format(self.id).encode())
            os.close(unexport_fd)
        except OSError as e:
            raise GPIOError(e.errno, "Unexporting GPIO: " + e.strerror) from OSError

    def _read(self):
        # Read value
        try:
            buf = os.read(self._fd, 2)
        except OSError as e:
            raise GPIOError(e.errno, "Reading GPIO: " + e.strerror) from OSError

        # Rewind
        try:
            os.lseek(self._fd, 0, os.SEEK_SET)
        except OSError as e:
            raise GPIOError(e.errno, "Rewinding GPIO: " + e.strerror) from OSError

        if buf[0] == b"0"[0]:
            return False
        if buf[0] == b"1"[0]:
            return True

        raise GPIOError(None, "Unknown GPIO value: {}".format(buf))

    def _write(self, value):
        if not isinstance(value, bool):
            raise TypeError("Invalid value type, should be bool.")

        # Write value
        try:
            if value:
                os.write(self._fd, b"1\n")
            else:
                os.write(self._fd, b"0\n")
        except OSError as e:
            raise GPIOError(e.errno, "Writing GPIO: " + e.strerror) from OSError

        # Rewind
        try:
            os.lseek(self._fd, 0, os.SEEK_SET)
        except OSError as e:
            raise GPIOError(e.errno, "Rewinding GPIO: " + e.strerror) from OSError

    @property
    def chip_name(self):
        """Return the Chip Name"""
        gpio_path = os.path.join(self._path, "device")

        gpiochip_path = os.readlink(gpio_path)

        if "/" not in gpiochip_path:
            raise GPIOError(
                None,
                'Reading gpiochip name: invalid device symlink "{:s}"'.format(
                    gpiochip_path
                ),
            )

        return gpiochip_path.split("/")[-1]

    @property
    def chip_label(self):
        """Return the Chip Label"""
        gpio_path = "/sys/class/gpio/{:s}/label".format(self.chip_name)

        try:
            with open(gpio_path, "r") as f_label:
                label = f_label.read()
        except (GPIOError, IOError) as e:
            if isinstance(e, IOError):
                raise GPIOError(
                    e.errno, "Reading gpiochip label: " + e.strerror
                ) from IOError

            raise GPIOError(
                None, "Reading gpiochip label: " + e.strerror
            ) from GPIOError

        return label.strip()

    # Mutable properties

    def _get_direction(self):
        # Read direction
        try:
            with open(os.path.join(self._path, "direction"), "r") as f_direction:
                direction = f_direction.read()
        except IOError as e:
            raise GPIOError(
                e.errno, "Getting GPIO direction: " + e.strerror
            ) from IOError

        return direction.strip()

    def _set_direction(self, direction):
        if not isinstance(direction, str):
            raise TypeError("Invalid direction type, should be string.")
        if direction.lower() not in ["in", "out", "high", "low"]:
            raise ValueError('Invalid direction, can be: "in", "out", "high", "low".')

        # Write direction
        try:
            with open(os.path.join(self._path, "direction"), "w") as f_direction:
                f_direction.write(direction.lower() + "\n")
        except IOError as e:
            raise GPIOError(
                e.errno, "Setting GPIO direction: " + e.strerror
            ) from IOError

    direction = property(_get_direction, _set_direction)

    def __str__(self):
        try:
            str_direction = self.direction
        except GPIOError:
            str_direction = "<error>"

        try:
            str_chip_name = self.chip_name
        except GPIOError:
            str_chip_name = "<error>"

        try:
            str_chip_label = self.chip_label
        except GPIOError:
            str_chip_label = "<error>"

        output = "Pin {:d} (dev={:s}, fd={:d}, dir={:s}, chip_name='{:s}', chip_label='{:s}')"
        return output.format(
            self.id, self._path, self._fd, str_direction, str_chip_name, str_chip_label
        )
