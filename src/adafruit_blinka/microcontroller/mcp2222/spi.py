# SPDX-FileCopyrightText: 2026 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""MCP2222 SPI with software-controlled peripheral chip selects."""

from pymcp2222 import IOPinConfig, IODirection, IO4Designation
from pymcp2222.exceptions import SPIError
from pymcp2222.spi import SPIParams, SPISpeed, SPIMode, SpiCs, SpiCsPolarity

from .mcp2222 import mcp2222
from .pin import Pin

_FREQUENCIES = (187500, 375000, 750000, 1500000, 3000000, 6000000, 12000000)


class SPI:
    """SPI transfers with G4 reserved as an unused hardware chip select."""

    MSB = 0

    def __init__(self):
        if Pin.spi_active:
            raise RuntimeError("MCP2222 SPI is already in use")
        self._closed = False
        self._frequency = 0
        self._saved_g4 = mcp2222.io.get_config(4)
        try:
            mcp2222.io.set_config(
                4, IOPinConfig(IO4Designation.CS0, IODirection.OUTPUT, idle_state=True)
            )
            self.init()
        except Exception:
            mcp2222.io.set_config(4, self._saved_g4)
            raise
        Pin.spi_active = True

    # Match the SPI backend interface used by busio.
    # pylint: disable=too-many-arguments
    def init(self, baudrate=187500, polarity=0, phase=0, bits=8, firstbit=MSB):
        """Select a supported frequency and one of the four SPI modes."""
        self._check_open()
        if baudrate <= 0:
            raise ValueError("baudrate must be positive")
        if polarity not in (0, 1) or phase not in (0, 1):
            raise ValueError("polarity and phase must be 0 or 1")
        if bits != 8 or firstbit != self.MSB:
            raise ValueError("MCP2222 SPI supports only 8-bit, MSB-first transfers")
        frequency = max(rate for rate in _FREQUENCIES if rate <= max(187500, baudrate))
        params = SPIParams(
            SPISpeed.from_hz(frequency),
            SPIMode(0x44 + 2 * polarity + phase),
            SpiCs.CS0,
            SpiCsPolarity.ACTIVE_LOW,
            0,
        )
        try:
            mcp2222.spi.configure(params)
        except SPIError as error:
            raise OSError(str(error)) from error
        self._frequency = frequency

    def _check_open(self):
        if self._closed:
            raise RuntimeError("SPI has been deinitialized")

    @property
    def frequency(self):
        """Return the actual hardware clock frequency in Hz."""
        self._check_open()
        return self._frequency

    def deinit(self):
        """Release SPI and restore G4's previous configuration."""
        if not self._closed:
            mcp2222.io.set_config(4, self._saved_g4)
            Pin.spi_active = False
            self._closed = True

    def write(self, buf, start=0, end=None):
        """Write a buffer slice."""
        self._check_open()
        data = bytes(memoryview(buf).cast("B")[start:end])
        if not data:
            return
        try:
            mcp2222.spi.write(data)
        except SPIError as error:
            raise OSError(str(error)) from error

    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read a buffer slice while transmitting the requested fill byte."""
        view = memoryview(buf).cast("B")[start:end]
        self.write_readinto(bytes([write_value]) * len(view), view)

    def write_readinto(
        self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None
    ):
        """Exchange equal-sized slices, including overlapping buffers."""
        self._check_open()
        data = bytes(memoryview(buffer_out).cast("B")[out_start:out_end])
        view = memoryview(buffer_in).cast("B")[in_start:in_end]
        if view.readonly:
            raise TypeError("Input buffer must be writable")
        if len(data) != len(view):
            raise ValueError("SPI buffer slices must be the same length")
        if not data:
            return
        try:
            received = mcp2222.spi.exchange(data)
        except SPIError as error:
            raise OSError(str(error)) from error
        if len(received) != len(view):
            raise OSError("Incomplete MCP2222 SPI transfer")
        view[:] = received
