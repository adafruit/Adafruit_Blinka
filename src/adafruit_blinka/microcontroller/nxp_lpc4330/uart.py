# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""UART Class for NXP LPC4330"""
from greatfet import GreatFET
from greatfet.interfaces.uart import UART as _UART


class UART:
    """Custom UART Class for NXP LPC4330"""

    PARITY_NONE = 0
    PARITY_ODD = 1
    PARITY_EVEN = 2
    PARITY_STUCK_AT_ONE = 3
    PARITY_STUCK_AT_ZERO = 4

    # pylint: disable=too-many-arguments,unused-argument
    def __init__(
        self,
        portid,
        baudrate=9600,
        bits=8,
        parity=None,
        stop=1,
        timeout=1000,
        read_buf_len=None,
        flow=None,
    ):
        self._gf = GreatFET()
        self._uart = _UART(
            self._gf,
            baud=baudrate,
            data_bits=bits,
            stop_bits=stop,
            parity=parity,
            uart_number=portid,
        )

        if flow is not None:  # default None
            raise NotImplementedError(
                "Parameter '{}' unsupported on GreatFET One".format("flow")
            )

    # pylint: enable=too-many-arguments,unused-argument

    def deinit(self):
        """Deinitialize"""
        self._uart.initialized = False

    def read(self, nbytes=None):
        """Read data from UART and return it"""
        if nbytes is None:
            return None
        return self._uart.read(nbytes)

    def readinto(self, buf, nbytes=None):
        """Read data from UART and into the buffer"""
        if nbytes is None:
            return None
        result = self.read(nbytes)
        for _ in range(nbytes):
            buf.append(result)
        return buf

    def readline(self):
        """Read a single line of data from UART"""
        out = self.read(nbytes=1)
        line = out
        while out != "\r":
            out = self.read(nbytes=1)
            line += out
        return line

    def write(self, buf):
        """Write data from the buffer to UART"""
        return self._uart.write(buf)
