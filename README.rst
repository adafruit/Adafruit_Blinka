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

This repository contains a selection of packages emulating the CircuitPython API
for devices or hosts running CPython or MicroPython. Working code exists to emulate these CircuitPython packages:

* **analogio** - analog input/output pins, using pin identities from board+microcontroller packages
* **bitbangio** - software-driven interfaces for I2C, SPI
* **board** - breakout-specific pin identities
* **busio** - hardware-driven interfaces for I2C, SPI, UART
* **digitalio** - digital input/output pins, using pin identities from board+microcontroller packages
* **keypad** - support for scanning keys and key matrices
* **microcontroller** - chip-specific pin identities
* **micropython** - MicroPython-specific module
* **neopixel_write** - low-level interface to NeoPixels
* **pulseio** - contains classes that provide access to basic pulse IO (PWM)
* **pwmio** - contains classes that provide access to basic pulse IO (PWM)
* **rainbowio** - provides the colorwheel() function
* **usb_hid** - act as a hid-device using usb_gadget kernel driver

For details, see the `Blinka API reference
<https://circuitpython.readthedocs.io/projects/blinka/en/latest/index.html>`_.

Dependencies
=============

The emulation described above is intended to provide a
CircuitPython-like API for devices which are running CPython or
Micropython. Since corresponding packages should be built-in to any
standard CircuitPython image, they have no value on a device already
running CircuitPython and would likely conflict in unhappy ways.

The test suites in the test/src folder under **testing.universal** are by design
intended to run on *either* CircuitPython *or* CPython/Micropython+compatibility layer to prove conformance.

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

The pin names may vary by board, so you may need to change the pin names in the code. This
example runs on the Raspberry Pi boards to blink an LED connected to GPIO 18 (Pin 12):

.. code-block:: python

    import time
    import board
    import digitalio

    PIN = board.D18

    print("hello blinky!")

    led = digitalio.DigitalInOut(PIN)
    led.direction = digitalio.Direction.OUTPUT

    while True:
        led.value = True
        time.sleep(0.5)
        led.value = False
        time.sleep(0.5)

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
