.. SPDX-FileCopyrightText: 2026 Limor Fried for Adafruit Industries
..
.. SPDX-License-Identifier: MIT

Implementation notes
====================

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
