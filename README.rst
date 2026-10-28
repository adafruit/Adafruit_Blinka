Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-micropython-blinka/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/blinka/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_Blinka/actions/workflows/build.yml/badge.svg
    :target: https://github.com/adafruit/Adafruit_Blinka/actions/workflows/build.yml
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

Blinka installs a platform-independent base package. On CPython, importing
``board`` checks the detected Raspberry Pi, Jetson, or AM33XX dependencies. An
interactive terminal offers to install missing or incompatible packages with
the running Python interpreter. Other boards retain their existing backend
selection and manual dependency setup; unrelated packages are not installed.

Non-interactive programs never prompt or run pip. A missing backend reports its
installation guidance when imported; a known incompatible installed version
of a required GPIO backend reports an actionable error rather than silently
continuing. PWM and NeoPixel backends are optional for ``board``: declining
their installation or encountering an installation failure does not block
unrelated GPIO use. Installation failures produce a warning, and missing or
known incompatible backends are reported when their feature is imported.
If an upgraded backend was already imported, restart Python before using the
replacement, even when that backend is optional.
After installation, Blinka rechecks imports and required versions. If they are
still unavailable (for example, after the first user-site installation), it
reports restart guidance rather than continuing as though installation fixed
the running process. Optional-only problems warn instead of aborting ``board``.

Use a virtual environment where practical. The runtime installer does not use
sudo, bypass externally managed environment protections, install OS packages,
or change GPIO permissions. Native packages may still need a compiler and Python
development headers provided by the operating system.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, install
`from PyPI <https://pypi.org/project/Adafruit-Blinka/>`_ in a virtual environment:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install Adafruit-Blinka

MCP2222 USB bridge
------------------

Install Microchip's transport library alongside Blinka::

    pip3 install Adafruit-Blinka "pymcp2222>=1.0.1.7"

Set ``BLINKA_MCP2222=1`` before importing ``board``. MCP2222 support provides
``board.SCL``, ``board.SDA``, and ``board.G0`` through ``board.G5`` for I2C and
digital GPIO with push-pull outputs and input pull-ups. SPI, open-drain outputs,
and the alternate pin functions are not implemented by this backend.

Scans and empty writes probe an address by writing one ``0x00`` byte, as in
MCP2221 scans; MCP2222 does not support address-only writes. Check that attached
devices tolerate this probe. The vendor library and OS must be able to access
the MCP2222 USB interface.

Environments created with uv
----------------------------

By default, ``uv venv`` does not install pip into the environment. Blinka's
automatic installer requires pip; it does not install pip or run uv for you.
If pip has no runnable entry point, a confirmed installation reports manual
recovery guidance without launching an installer. Missing optional PWM/NeoPixel
packages still do not block unrelated GPIO use.

Use uv to install the required backends into the same environment. For Raspberry
Pi GPIO, for example:

.. code-block:: shell

    uv venv .env
    uv pip install --python .env/bin/python Adafruit-Blinka 'gpiod>=2.2.2,<3'

Add the PWM or NeoPixel backend if needed, and run your program with
``.env/bin/python``. Manual recovery commands use the running interpreter's path
so an unrelated active environment is not selected. After installing dependencies
while Python is running, restart it before trying again. See uv's
`Python environment documentation
<https://docs.astral.sh/uv/pip/environments/#using-arbitrary-python-environments>`_.
For pip-backed interactive installation, create the environment with
``uv venv --seed .env`` instead.

Services and managed environments
---------------------------------

Install the backends your program needs before starting a service, cron job, or
other non-interactive program. For Raspberry Pi digital GPIO, for example:

.. code-block:: shell

    .env/bin/python -m pip install Adafruit-Blinka 'gpiod>=2.2.2,<3'

If the program also uses PWM, install its backend during setup:

.. code-block:: shell

    .env/bin/python -m pip install 'Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2'

Run the service with that same environment's Python. A virtual environment using
``--system-site-packages`` can see OS packages, but those packages must still
meet the required versions. Blinka does not bypass externally managed system
Python protections.

For Raspberry Pi GPIO, Blinka also accepts Debian-style ``python3-libgpiod``
bindings labelled ``2.2.0`` when they come from maintained libgpiod source
``>=2.2.1,<3`` and report a native API version in that range. Trixie's package
uses this older Python label despite containing later fixes. In a virtual
environment created with ``--system-site-packages``, Blinka checks that the
selected binding and metadata paths belong to the installed system package.
Security-update revisions are not pinned, and importing ``gpiod`` before
``board`` works normally. Package-manager queries are cached per process.

This trusts the system administrator and package database; it is not a file
integrity monitor. Restart Python after package upgrades rather than reloading
native modules. Ordinary PyPI installs retain the conservative
``gpiod>=2.2.2,<3`` baseline: old PyPI ``2.2.0`` has a native use-after-free
during line requests, which a check for available API functions cannot detect.
See the `upstream fix
<https://github.com/brgl/libgpiod/commit/c497e29ca1f88963c525351e60af23ed896a2b8c>`_.

For an application that manages its own dependencies, set
``BLINKA_SKIP_DEPENDENCY_CHECK=1`` before importing ``board`` to disable its
automatic dependency checks and installation prompts:

.. code-block:: shell

    BLINKA_SKIP_DEPENDENCY_CHECK=1 .env/bin/python program.py

This does not install packages or make unsupported backends supported. Missing
backend imports and PWM/NeoPixel feature checks still report errors.

Installing on MicroPython
=========================

The root ``package.json`` installs Blinka's existing MicroPython subset directly
from GitHub with `mip <https://docs.micropython.org/en/latest/reference/packages.html>`_.
From a computer with the board connected, run:

.. code-block:: shell

    mpremote mip install github:adafruit/Adafruit_Blinka

On firmware that includes ``mip`` and has a working network connection, you can
instead install from the MicroPython REPL:

.. code-block:: python

    import mip
    mip.install("github:adafruit/Adafruit_Blinka")

Restart the board after installing. To select a release or branch, append
``@TAG_OR_BRANCH`` to the ``mpremote`` URL, or pass ``version="TAG_OR_BRANCH"``
to ``mip.install``. Choose a ref containing ``package.json``; older releases do
not have this manifest. Installation needs network access to GitHub on the
computer (``mpremote``) or board (``mip``). This is not a PyPI install or a
short-name package in the default MicroPython package index.

The manifest includes ``board``, ``microcontroller``, ``digitalio``, ``busio``,
``bitbangio``, and ``rainbowio``, plus the existing Pico-family, Pyboard, and
ESP8266 board routes. It installs only the required PlatformDetect source files,
pinned to release 3.89.1, and their licenses. Linux drivers, native binaries,
pip dependencies, and the CPython ``micropython`` shim are not installed.
The installed file contents total about 190 KiB, plus filesystem overhead.
When updating PlatformDetect, update all its manifest URLs together to the new
release's commit; absolute pinned URLs keep Blinka branch/tag installs from
accidentally selecting the same ref in another repository.

This packages existing backends, not new hardware or API support. Not every
CircuitPython module is implemented on MicroPython, and existing backend/firmware
limitations still apply. In particular, the legacy ESP8266 backend's ``TOUT``
pin initialization is incompatible with current MicroPython firmware. Source
compilation also requires RAM in addition to filesystem space; small boards
such as ESP8266 may not have enough. Install CircuitPython libraries needed by
your application separately, and verify compatibility on your board. Do not
install Blinka on CircuitPython itself.

Raspberry Pi GPIO and PWM
=========================

Raspberry Pi digital GPIO uses the official ``gpiod`` bindings. ``pwmio.PWMOut``
uses `Adafruit Blinka Raspberry Pi PWM
<https://github.com/adafruit/Adafruit_Blinka_Raspberry_Pi_PWM>`_ on Pi 5 and earlier
models. Configured BCM/RP1 hardware PWM is preferred on verified pin routes;
other pins use native software PWM. This does not use PIO or change boot overlays.
Runtime checks select ``gpiod>=2.2.2,<3`` and
``Adafruit-Blinka-Raspberry-Pi-PWM>=1.0.2`` only for Raspberry Pi boards, rather
than installing them on every Linux ARM host. These Pi backends require Linux
5.10 or newer. NeoPixel support retains its separate dependencies.

Software PWM accepts 1--10000 Hz, with Linux scheduling affecting timing and
jitter. Configured hardware limits depend on its controller and driver, and
updates are not guaranteed glitch-free. Hardware channels require separate
kernel/overlay configuration and sysfs permissions. See the package's
`usage guide <https://github.com/adafruit/Adafruit_Blinka_Raspberry_Pi_PWM/blob/main/docs/usage.rst>`_
for setup and cleanup limitations; verify the waveform before connecting an
actuator. NeoPixel support continues to use its existing separate backends.

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
