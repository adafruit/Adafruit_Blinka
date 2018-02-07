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

.. todo:: Describe what the library does.

Dependencies
=============
This driver depends on:

* Micropython

Usage Example
=============

.. todo:: Add a quick, simple example. It and other examples should live in the examples folder and be included in docs/examples.rst.

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
