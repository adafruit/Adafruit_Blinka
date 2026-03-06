# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_blinka.importing` - Import utilities that run on Linux and MicroPython
======================================================================================

* Author(s): Melissa LeBlanc-Williams
"""

try:
    from importlib import import_module
except ImportError as e:

    def import_module(module_name: str, package: str = None):
        """importlib not available, define an alternate import_module function"""
        package_list = []
        if package is not None:
            package_list.append(package)
        return __import__(module_name, globals(), locals(), package_list)


def get_import_file(json_file_name, script_file_location):
    """Get the full path to the microcontroller imports file."""
    try:
        from pathlib import Path

        script_folder = Path(script_file_location).parent.absolute()
        return script_folder / json_file_name
    except ImportError:
        # MicroPython doesn't have pathlib, so we have to do it manually
        if script_file_location.startswith("/"):
            script_folder = "/".join(script_file_location.split("/")[:-1])
        else:
            script_folder = "."
        return f"{script_folder}/{json_file_name}"


def import_mod(caller_globals, module_name: str, package_name: str = "*"):
    """Function to allow importing with * or specific package name."""
    if package_name == "*":
        module = import_module(module_name)
        caller_globals.update(
            {name: getattr(module, name) for name in module.__all__}
            if hasattr(module, "__all__")
            else {
                key: value
                for (key, value) in module.__dict__.items()
                if not key.startswith("_")
            }
        )
    else:
        import_module(module_name, package=package_name)
