# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Generic Connection class for Binho Nova to keep track of connection"""


class Connection:
    """Connection class"""

    __instance = None

    @staticmethod
    def getInstance():
        """Static access method."""
        if Connection.__instance is None:
            Connection()
        return Connection.__instance

    def __init__(self):
        """Virtually private constructor."""
        if Connection.__instance is not None:
            raise Exception(  # pylint: disable=broad-exception-raised
                "This class is a singleton!"
            )

        # pylint: disable=import-outside-toplevel
        from binhoHostAdapter import binhoHostAdapter
        from binhoHostAdapter import binhoUtilities

        # pylint: enable=import-outside-toplevel
        devices = binhoUtilities.listAvailableDevices()

        if len(devices) > 0:
            Connection.__instance = binhoHostAdapter.binhoHostAdapter(devices[0])
        else:
            raise RuntimeError("No Binho Nova found!")
