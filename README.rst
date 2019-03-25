Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-micropython-blinka/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/blinka/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_Blinka.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_Blinka
    :alt: Build Status

This repository contains a selection of packages mirroring the CircuitPython API
on hosts running micropython. Working code exists to emulate the CircuitPython packages;

* **board** - breakout-specific pin identities
* **microcontroller** - chip-specific pin identities
* **digitalio** - digital input/output pins, using pin identities from board+microcontroller packages
* **bitbangio** - software-driven interfaces for I2C, SPI
* **busio** - hardware-driven interfaces for I2C, SPI, UART
* **time** * - substitute functions monkey-patched to time module


Dependencies
=============

The Micropython compatibility layers described above are intended to provide a CircuitPython-like API for devices which
are running CPython or Micropython. Since corresponding packages should be built-in to any standard
CircuitPython image, they have no value on a device already running CircuitPython and would likely conflict in unhappy ways.

The test suites in the test/src folder under **testing.universal** are by design
intended to run on *either* CircuitPython *or* Micropython+compatibility layer to prove conformance.

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
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
