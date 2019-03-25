#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

setup(
    name='Adafruit-Blinka',
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description='CircuitPython APIs for non-CircuitPython versions of Python such as CPython on Linux and MicroPython.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Adafruit Industries',
    author_email='circuitpython@adafruit.com',
    python_requires='>=3.4.0',
    url='https://github.com/adafruit/Adafruit_Blinka',
    package_dir={'': 'src'},
    packages=find_packages("src"),
    # py_modules lists top-level single file packages to include.
    # find_packages only finds packages in directories with __init__.py files.
    py_modules=['bitbangio', 'board', 'busio', 'digitalio', 'micropython', 'pulseio', 'neopixel_write'],
    package_data={'adafruit_blinka.microcontroller.bcm283x.pulseio': ['libgpiod_pulsein']},
    install_requires=[
        "Adafruit-PlatformDetect",
        "Adafruit-PureIO",
        "RPi.GPIO; platform_machine=='armv7l' or platform_machine=='armv6l'",
        "rpi_ws281x>=4.0.0; platform_machine=='armv7l' or platform_machine=='armv6l'",
        "spidev; sys_platform=='linux'",
        "sysv_ipc; platform_system != 'Windows'"
    ],
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: MicroPython',
    ],
)
