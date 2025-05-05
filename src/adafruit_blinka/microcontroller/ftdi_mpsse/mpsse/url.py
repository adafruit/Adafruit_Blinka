# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Support for getting the URL from the BLINKA_FT232H
and BLINKA_FTX232H_{} environment variables.
"""

import os


def get_ft232h_url():
    """
    Return the FTDI url to use. If BLINKA_FT232H starts with ftdi:, returns
    that. Otherwise, returns a default value.
    """

    url = os.environ.get("BLINKA_FT232H", "1")

    if url.startswith("ftdi:"):
        return url

    return "ftdi://ftdi:ft232h/1"


def get_ftx232h_url(interface_id):
    """
    Return the FTDI url to use. If BLINKA_FTX232H_{} starts with ftdi:, returns
    that. Otherwise, returns a default value.
    """

    url = os.environ.get("BLINKA_FTX232H_{}".format(interface_id), "1")

    if url.startswith("ftdi:"):
        return url

    if os.environ.get("BLINKA_FT2232H", None):
        return "ftdi://ftdi:ft2232h/{}".format(interface_id + 1)
    return "ftdi://ftdi:ft4232h/{}".format(interface_id + 1)
