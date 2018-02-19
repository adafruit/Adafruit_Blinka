Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-micropython-blinka/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/blinka/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.org/adafruit/Adafruit_Micropython_Blinka.svg?branch=master
    :target: https://travis-ci.org/adafruit/Adafruit__Micropython_Blinka
    :alt: Build Status

This repository contains a selection of packages mirroring the CircuitPython API
on hosts running micropython. Working code exists to emulate the CircuitPython packages;

* **board** - breakout-specific pin identities
* **microcontroller** - chip-specific pin identities
* **digitalio** - digital input/output pins, using pin identities from board+microcontroller packages


Dependencies
=============

The Micropython compatibility layers described above are intended to provide a CircuitPython-like API for devices which
are running Micropython. Since corresponding packages should be built-in to any standard
CircuitPython image, they have no value on a device already running CircuitPython and would likely conflict in unhappy ways.

The test suites under **testing.implementation.all** are by design
intended to run on *either* CircuitPython *or* Micropython+compatibility layer to prove conformance. 

The test suites under **testing.implementation.micropython** will only run
on Micropython and **testing.implementation.circuitpython** will only run on CircuitPython


Usage Example
=============

At the time of writing (`git:3b2fc268 <https://github.com/cefn/Adafruit_Micropython_Blinka/tree/3b2fc268d89aee6a648da456224e6d48d2476baa>`_),
the following sequence runs through some basic testing of the digitalio compatibility layer, which looks like `this <https://github.com/cefn/Adafruit_Micropython_Blinka/issues/2#issuecomment-366713394>`_ .

.. code-block:: python

    import testing
    testing.main()


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_Micropython_Blinka/blob/master/CODE_OF_CONDUCT.md>`_
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
