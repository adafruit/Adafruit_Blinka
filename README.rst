Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-micropython-blinka/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/blinka/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_Blinka.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_Blinka
    :alt: Build Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

This repository contains a selection of packages mirroring the CircuitPython API
on hosts running micropython. Working code exists to emulate the CircuitPython packages;

* **board** - breakout-specific pin identities
* **microcontroller** - chip-specific pin identities
* **analogio** - analog input/output pins, using pin identities from board+microcontroller packages
* **digitalio** - digital input/output pins, using pin identities from board+microcontroller packages
* **bitbangio** - software-driven interfaces for I2C, SPI
* **busio** - hardware-driven interfaces for I2C, SPI, UART
* **pulseio** - contains classes that provide access to basic pulse IO (PWM)

For details, see the `Blinka API reference
<https://circuitpython.readthedocs.io/projects/blinka/en/latest/index.html>`_.

Dependencies
=============

The Micropython compatibility layers described above are intended to provide a CircuitPython-like API for devices which
are running CPython or Micropython. Since corresponding packages should be built-in to any standard
CircuitPython image, they have no value on a device already running CircuitPython and would likely conflict in unhappy ways.

The test suites in the test/src folder under **testing.universal** are by design
intended to run on *either* CircuitPython *or* Micropython+compatibility layer to prove conformance.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/Adafruit-Blinka/>`_. To install for current user:

.. code-block:: shell

    pip3 install Adafruit-Blinka

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install Adafruit-Blinka

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install Adafruit-Blinka

Usage Example
=============

At the time of writing (`git:7fc1f8ab <https://github.com/cefn/Adafruit_Micropython_Blinka/tree/7fc1f8ab477124628a5afebbf6826005955805f9>`_),
the following sequence runs through some basic testing of the digitalio compatibility layer...

.. code-block:: python

    from testing import test_module_name
    test_module_name("testing.universal.digitalio")

An example log from running the suites is `here <https://github.com/cefn/Adafruit_Micropython_Blinka/issues/2#issuecomment-366713394>`_ .

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_Blinka/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme Adafruit-PlatformDetect

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
