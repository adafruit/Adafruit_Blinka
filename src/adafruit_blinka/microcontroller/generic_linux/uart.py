# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Generic Linux UART class wrapping PySerial"""

import os

import serial


class UART:
    """UART class for generic Linux using PySerial.

    Wraps a ``serial.Serial`` instance so that CircuitPython UART code
    runs unchanged on Linux / SBC boards.
    """

    # Map of known port IDs to device paths, by platform.
    # If the port entry in uartPorts is a string it is used directly;
    # otherwise we try common symlink / device conventions.
    _PORT_SEARCH_PATTERNS = (
        "/dev/serial{}",
        "/dev/ttyS{}",
        "/dev/ttyAMA{}",
    )

    def __init__(
        self,
        port_id,
        baudrate=9600,
        bits=8,
        parity=None,
        stop=1,
        timeout=1,
        receiver_buffer_size=64,
    ):
        device = self._resolve_device(port_id)

        # Translate CircuitPython parity values to pyserial constants.
        if parity is None:
            ser_parity = serial.PARITY_NONE
        elif parity == 0:
            ser_parity = serial.PARITY_EVEN
        elif parity == 1:
            ser_parity = serial.PARITY_ODD
        else:
            raise ValueError("Invalid parity: {}".format(parity))

        stop_map = {1: serial.STOPBITS_ONE, 2: serial.STOPBITS_TWO}
        ser_stop = stop_map.get(stop)
        if ser_stop is None:
            raise ValueError("Invalid stop bits: {}".format(stop))

        byte_size_map = {
            5: serial.FIVEBITS,
            6: serial.SIXBITS,
            7: serial.SEVENBITS,
            8: serial.EIGHTBITS,
        }
        ser_bytesize = byte_size_map.get(bits)
        if ser_bytesize is None:
            raise ValueError("Invalid bits: {}".format(bits))

        # PySerial timeout is in seconds (float); CircuitPython also uses
        # seconds as of CP 4.0+.  Blinka's older MicroPython path passed
        # timeout in *milliseconds* to machine.UART; we accept seconds here.
        self._serial = serial.Serial(
            device,
            baudrate=baudrate,
            bytesize=ser_bytesize,
            parity=ser_parity,
            stopbits=ser_stop,
            timeout=timeout,
            write_timeout=timeout,
        )

    # ----- helpers -----

    @classmethod
    def _resolve_device(cls, port_id):
        """Turn a port identifier into a ``/dev/`` path.

        *port_id* may be:
        - A string that is already a device path (e.g. ``"/dev/serial0"``).
        - An integer that will be resolved via common naming conventions.
        """
        if isinstance(port_id, str) and os.path.exists(port_id):
            return port_id

        if isinstance(port_id, int):
            for pattern in cls._PORT_SEARCH_PATTERNS:
                path = pattern.format(port_id)
                if os.path.exists(path):
                    return path

        raise RuntimeError(
            "Could not find UART device for port {!r}.  "
            "Make sure the serial port is enabled.".format(port_id)
        )

    # ----- CircuitPython-compatible API -----

    def deinit(self):
        """Close the serial port."""
        if self._serial is not None:
            self._serial.close()
            self._serial = None

    def read(self, nbytes=None):
        """Read up to *nbytes* bytes.  Returns ``None`` when no data is
        available (matching CircuitPython behaviour, not pyserial's ``b""``).
        """
        if nbytes is None:
            # Read whatever is available; if nothing, wait up to timeout.
            data = self._serial.read(self._serial.in_waiting or 1)
        else:
            data = self._serial.read(nbytes)
        return data if data else None

    def readinto(self, buf, nbytes=None):
        """Read bytes into *buf*.  Returns number of bytes read or ``None``."""
        if nbytes is None:
            nbytes = len(buf)
        data = self._serial.read(nbytes)
        if not data:
            return None
        n = len(data)
        buf[:n] = data
        return n

    def readline(self):
        """Read a line (up to ``\\n``).  Returns ``None`` on timeout with no data."""
        data = self._serial.readline()
        return data if data else None

    def write(self, buf):
        """Write bytes from *buf*.  Returns the number of bytes written."""
        return self._serial.write(buf)

    @property
    def baudrate(self):
        """The current baudrate."""
        return self._serial.baudrate

    @baudrate.setter
    def baudrate(self, value):
        self._serial.baudrate = value

    @property
    def in_waiting(self):
        """The number of bytes in the input buffer, available to be read."""
        return self._serial.in_waiting

    @property
    def timeout(self):
        """Read timeout in seconds (float)."""
        return self._serial.timeout

    @timeout.setter
    def timeout(self, value):
        self._serial.timeout = value
        self._serial.write_timeout = value

    def reset_input_buffer(self):
        """Discard any unread data in the input buffer."""
        self._serial.reset_input_buffer()
