#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

board_reqs = []
if os.path.exists("/proc/device-tree/compatible"):
    with open("/proc/device-tree/compatible", "rb") as f:
        compat = f.read()
    # Jetson Nano, TX2, Xavier, etc
    if b"nvidia,tegra" in compat:
        board_reqs = ["Jetson.GPIO"]
    # Pi 5 and Earlier
    elif (
        b"brcm,bcm2835" in compat
        or b"brcm,bcm2836" in compat
        or b"brcm,bcm2837" in compat
        or b"brcm,bcm2838" in compat
        or b"brcm,bcm2711" in compat
        or b"brcm,bcm2712" in compat
    ):
        _pyver = (sys.version_info.major, sys.version_info.minor)
        _machine = os.uname().machine
        # Pre-built URL wheels for Python 3.13-3.15 aarch64 (no PyPI wheel, swig not required)
        _lgpio_url_versions = {(3, 13), (3, 14), (3, 15)}
        if _pyver in _lgpio_url_versions and _machine == "aarch64":
            _pytag = f"cp{_pyver[0]}{_pyver[1]}"
            lgpio_req = (
                "lgpio @ https://github.com/adafruit/lgpio-python-wheels/raw/main/"
                f"wheels/lgpio-0.2.2.0-{_pytag}-{_pytag}-linux_aarch64.whl"
            )
        else:
            lgpio_req = "lgpio>=0.2.2.0"
        try:
            import lgpio
        except ImportError:
            print(
                "\n*** lgpio is not installed. On Raspberry Pi OS, install it with:\n"
                "    sudo apt-get install -y python3-lgpio\n"
                "  Then recreate your virtual environment with --system-site-packages\n"
                "  or install the wheel from:\n"
                "    https://github.com/adafruit/lgpio-python-wheels\n"
            )
        board_reqs = [
            "rpi_ws281x>=4.0.0",
            lgpio_req,
            "RPi.GPIO",
            "Adafruit-Blinka-Raspberry-Pi5-Neopixel",
        ]
    # BeagleBone Black, Green, PocketBeagle, BeagleBone AI, etc.
    elif b"ti,am335x" in compat:
        board_reqs = ["Adafruit_BBIO"]

setup(
    name="Adafruit-Blinka",
    use_scm_version={
        # This is needed for the PyPI version munging in the Github Actions release.yml
        "git_describe_command": "git describe --tags --long",
        "local_scheme": "no-local-version",
    },
    description="CircuitPython APIs for non-CircuitPython versions of Python such as CPython on Linux and MicroPython.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Adafruit Industries",
    author_email="circuitpython@adafruit.com",
    python_requires=">=3.9.0",
    url="https://github.com/adafruit/Adafruit_Blinka",
    package_dir={"": "src"},
    packages=find_packages("src") + ["micropython-stubs"],
    # py_modules lists top-level single file packages to include.
    # find_packages only finds packages in directories with __init__.py files.
    py_modules=[
        "analogio",
        "bitbangio",
        "board",
        "busio",
        "digitalio",
        "keypad",
        "micropython",
        "neopixel_write",
        "onewireio",
        "pulseio",
        "pwmio",
        "rainbowio",
        "usb_hid",
    ],
    package_data={
        "adafruit_blinka": [
            "../board_imports.json",
            "../microcontroller_imports.json",
        ],
        "adafruit_blinka.microcontroller.bcm283x.pulseio": [
            "libgpiod_pulsein",
            "libgpiod_pulsein64",
        ],
        "adafruit_blinka.microcontroller.amlogic.meson_g12_common.pulseio": [
            "libgpiod_pulsein",
        ],
        "micropython-stubs": ["*.pyi"],
    },
    include_package_data=True,
    install_requires=[
        "Adafruit-PlatformDetect>=3.89.1",
        "Adafruit-PureIO>=1.1.7",
        "binho-host-adapter>=0.1.6",
        "pyftdi>=0.40.0",
        "adafruit-circuitpython-typing",
        "sysv_ipc>=1.1.0;sys_platform=='linux' and platform_machine!='mips'",
        "toml>=0.10.2;python_version<'3.11'",
    ]
    + board_reqs,
    license="MIT",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: MicroPython",
    ],
)
