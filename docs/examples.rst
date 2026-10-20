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
