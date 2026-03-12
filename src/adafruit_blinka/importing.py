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


from adafruit_blinka.agnostic import detector


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
        module = import_module(module_name, package=package_name)
        caller_globals[package_name] = getattr(module, package_name)


def import_microcontroller(
    caller_globals,
    microcontroller_imports,
    module_extension: str = "",
    package_name: str = "*",
):
    """Detect and import the microcontroller module and package based on detected hardware"""
    if module_extension[0:1] != "." and module_extension != "":
        # Make sure the module extension starts with a dot if it's not empty
        module_extension = f".{module_extension}"
    for chip_key, chip_module in microcontroller_imports.items():
        if getattr(detector.chip, chip_key):
            if isinstance(chip_module, dict):
                # Loop through the children and import the first one that matches
                for board_key, board_chip_module in chip_module.items():
                    if board_key.startswith("any_") and getattr(
                        detector.board, board_key
                    ):
                        # import Pin from the microcontroller module
                        import_mod(
                            caller_globals,
                            f"{board_chip_module}{module_extension}",
                            package_name,
                        )
                        return True
                    if board_key == getattr(detector.board, board_key):
                        print(f"Detected board: {board_key}")
                        import_mod(
                            caller_globals,
                            f"{board_chip_module}{module_extension}",
                            package_name,
                        )
                        return True
                import_mod(
                    caller_globals,
                    f"{chip_module['default']}{module_extension}",
                    package_name,
                )
                return True
            import_mod(caller_globals, f"{chip_module}{module_extension}", package_name)
            return True
    return False
