Examples
--------

See the `CircuitPython docs <https://circuitpython.readthedocs.io/>`_ for extensive API documentation which should
(mostly) work with Blinka.

.. literalinclude:: ../examples/analog_in.py
    :caption: examples/analog_in.py
    :linenos:

.. literalinclude:: ../examples/bbb_digitalio.py
    :caption: examples/bbb_digitalio.py
    :linenos:

.. literalinclude:: ../examples/mcps_busio_i2c.py
    :caption: examples/mcps_busio_i2c.py
    :linenos:

.. literalinclude:: ../examples/pb_digitalio.py
    :caption: examples/pb_digitalio.py
    :linenos:

.. literalinclude:: ../examples/pi_busio_i2c.py
    :caption: examples/pi_busio_i2c.py
    :linenos:

.. literalinclude:: ../examples/pi_busio_spi.py
    :caption: examples/pi_busio_spi.py
    :linenos:

.. literalinclude:: ../examples/pi_digitalio.py
    :caption: examples/pi_digitalio.py
    :linenos:

.. literalinclude:: ../examples/piblinka.py
    :caption: examples/piblinka.py
    :linenos:

.. literalinclude:: ../examples/usb_hid_keyboard.py
    :caption: examples/usb_hid_keyboard.py
    :linenos:

MCP2221 USB error recovery
~~~~~~~~~~~~~~~~~~~~~~~~~~

After an incomplete or interrupted USB HID exchange, reconnect the MCP2221
and restart the program before using it again. An old response can remain
queued, and the protocol has no transaction identifier to distinguish it
from a new response to the same command. Blinka therefore rejects further
transfers on that instance rather than guessing that the connection recovered.
It does not automatically retry commands, drain replies, or reset the device.
A failed exchange may already have changed the device's outputs; reporting
the error does not roll back its effects.

This applies to USB transport failures, not ordinary I2C busy or NACK
responses. Complete, matching responses still use the existing I2C error
handling, and scans continue past unsuccessful address probes. A transport
failure aborts the scan instead of appearing as an empty or partial device list.

MCP2221 activity LEDs
~~~~~~~~~~~~~~~~~~~~~

The MCP2221 exposes chip-specific, autonomous activity indicators on G0
(UART receive), G1 (UART transmit), and G3 (I2C). These do not change the
CircuitPython-facing ``digitalio`` or ``busio`` APIs. Pin assignments and
active-low signaling are described in the `MCP2221A datasheet
<https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/MCP2221A-Data-Sheet-20005565E.pdf>`_
(Table 1-5 and Sections 1.7.1.4--1.7.1.6).

.. literalinclude:: ../examples/mcp2221_activity_leds.py
    :caption: examples/mcp2221_activity_leds.py
    :linenos:

MCP2222 touchpaint
~~~~~~~~~~~~~~~~~~

Use an MCP2222 USB bridge with the ST7796S/FT6336U version of the 3.5-inch
capacitive TFT FeatherWing. The example includes wiring and installation
instructions and uses SPI for the display, I2C for touch, and GPIO for IRQ
and backlight control.

.. literalinclude:: ../examples/mcp2222_touchpaint.py
    :caption: examples/mcp2222_touchpaint.py
    :linenos:
