# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`adafruit_blinka` - Runtime utility objects for re-implementation of CircuitPython API
======================================================================================

* Author(s): cefn
"""

import os


class Enum:
    """
    Object supporting CircuitPython-style of static symbols
    as seen with Direction.OUTPUT, Pull.UP
    """

    def __repr__(self):
        """
        Assumes instance will be found as attribute of own class.
        Returns dot-subscripted path to instance
        (assuming absolute import of containing package)
        """
        cls = type(self)
        for key in dir(cls):
            if getattr(cls, key) is self:
                return "{}.{}.{}".format(cls.__module__, cls.__qualname__, key)
        return repr(self)

    @classmethod
    def iteritems(cls):
        """
        Inspects attributes of the class for instances of the class
        and returns as key,value pairs mirroring dict#iteritems
        """
        for key in dir(cls):
            val = getattr(cls, key)
            if isinstance(cls, val):
                yield (key, val)


class ContextManaged:
    """An object that automatically deinitializes hardware with a context manager."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()

    # pylint: disable=no-self-use
    def deinit(self):
        """Free any hardware used by the object."""
        return

    # pylint: enable=no-self-use


class Lockable(ContextManaged):
    """An object that must be locked to prevent collisions on a microcontroller resource."""

    _locked = False

    def try_lock(self):
        """Attempt to grab the lock. Return True on success, False if the lock is already taken."""
        if self._locked:
            return False
        self._locked = True
        return True

    def unlock(self):
        """Release the lock so others may use the resource."""
        if self._locked:
            self._locked = False


def load_settings_toml():
    """Load values from settings.toml into os.environ, so that os.getenv returns them.
    Note: This does not work in MicroPython because of the tomllib module not being available.
    """
    try:
        import tomllib
    except ImportError:
        import toml as tomllib

    if not os.path.isfile("settings.toml"):
        raise FileNotFoundError("settings.toml not found in current directory.")

    print("settings.toml found. Updating environment variables:")
    with open("settings.toml", "rb") as toml_file:
        try:
            settings = tomllib.load(toml_file)
        except tomllib.TOMLDecodeError as e:
            raise tomllib.TOMLDecodeError("Error with settings.toml file.") from e

    invalid_types = set()
    for key, value in settings.items():
        if not isinstance(value, (bool, int, float, str)):
            invalid_types.add(type(value).__name__)
    if invalid_types:
        invalid_types_string = ", ".join(invalid_types)
        raise ValueError(
            f"The types: '{invalid_types_string}' are not supported in settings.toml."
        )

    for key, value in settings.items():
        key = str(key)
        if key in os.environ:
            print(f" - {key} already exists in environment")
            continue
        os.environ[key] = str(value)
        print(f" - {key} added")

    return settings


def patch_system():
    """Patch modules that may be different due to the platform."""
    # pylint: disable=import-outside-toplevel
    import sys
    from adafruit_blinka.agnostic import time

    # pylint: enable=import-outside-toplevel

    sys.modules["time"] = time
