"""Support for getting the URL from the BLINKA_FT232H variable."""

import os


def get_ftdi_url():
    """
    Return the FTDI url to use. If BLINKA_FT232H starts with ftdi:, returns
    that. Otherwise, returns a default value.
    """

    url = os.environ.get("BLINKA_FT232H", "1")

    if url.startswith("ftdi:"):
        return url

    return "ftdi://ftdi:ft232h/1"
