#!/usr/bin/env python
# -*- coding: utf-8 -*-

# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

with io.open(os.path.join(here, "requirements.txt"), encoding="utf-8") as f:
    requirements = [
        line.strip()
        for line in f.readlines()
        if line.strip() and not line.startswith("#")
    ]

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
    install_requires=requirements,
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
