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
digital GPIO with push-pull outputs and input pull-ups. Open-drain outputs and
the other alternate pin functions are not implemented by this backend.

Scans and empty writes probe an address by writing one ``0x00`` byte, as in
MCP2221 scans; MCP2222 does not support address-only writes. Check that attached
devices tolerate this probe. The vendor library and OS must be able to access
the MCP2222 USB interface.

SPI
~~~

Use ``board.SPI()`` or ``busio.SPI(board.SCK, board.MOSI, board.MISO)``.
All four SPI modes are supported with 8-bit, MSB-first transfers. Supported
clock rates are 187.5 kHz, 375 kHz, 750 kHz, 1.5 MHz, 3 MHz, 6 MHz, and 12 MHz.
Requests round down to a supported rate, with a minimum of 187.5 kHz;
``spi.frequency`` reports the actual rate. Each transfer supports up to 65535
bytes, including sliced buffers and full-duplex ``write_readinto``.

The MCP2222 requires a hardware chip select, so SPI reserves **G4/CS0**.
Leave G4 disconnected from peripherals and use another GPIO, such as G0, with
``adafruit_bus_device.spi_device.SPIDevice`` for their chip select. This keeps
the peripheral selected across multiple SPI calls even though the unused
hardware CS toggles for each transfer. G4 cannot be used through ``digitalio``
while SPI is active; ``spi.deinit()`` restores its previous configuration.
