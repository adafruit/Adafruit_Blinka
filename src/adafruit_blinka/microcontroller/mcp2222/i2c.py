# SPDX-FileCopyrightText: 2026 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""I2C support for MCP2222 using Microchip's USB driver."""

from pymcp2222 import I2CParams, I2CSpeed
from pymcp2222.exceptions import I2CAddressNackError, I2CError

from .mcp2222 import mcp2222


class I2C:
    """CircuitPython I2C transfers through an MCP2222."""

    def __init__(self, *, frequency=100000):
        self._i2c = mcp2222.i2c
        self._i2c.configure(I2CParams(I2CSpeed.from_hz(frequency), 25))

    def scan(self):
        """Scan the non-reserved addresses using a one-byte write."""
        found = []
        for address in range(0x08, 0x78):
            try:
                self._i2c.write(address, b"\x00")
            except I2CAddressNackError:
                continue
            except I2CError as error:
                raise OSError(str(error)) from error
            found.append(address)
        return found

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        """Write a buffer slice, or probe with a one-byte write."""
        if not stop:
            raise NotImplementedError("Use writeto_then_readfrom for a repeated start")
        data = bytes(memoryview(buffer)[start:end])
        # MCP2222 cannot send an address-only write. Use the MCP2221 scan probe.
        if not data:
            data = b"\x00"
        try:
            self._i2c.write(address, data)
        except I2CError as error:
            raise OSError(str(error)) from error

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
        """Read into a buffer slice."""
        if not stop:
            raise NotImplementedError("Reads without a stop are not supported")
        view = memoryview(buffer)[start:end]
        if not view:
            return
        try:
            view[:] = self._i2c.read(address, len(view))
        except I2CError as error:
            raise OSError(str(error)) from error

    def writeto_then_readfrom(
        self,
        address,
        buffer_out,
        buffer_in,
        *,
        out_start=0,
        out_end=None,
        in_start=0,
        in_end=None,
        stop=False,
    ):
        """Write and read with a repeated start, or an optional intervening stop."""
        data = bytes(memoryview(buffer_out)[out_start:out_end])
        view = memoryview(buffer_in)[in_start:in_end]
        if not data:
            self.readfrom_into(address, view)
        elif not view:
            self.writeto(address, data)
        elif stop:
            self.writeto(address, data)
            self.readfrom_into(address, view)
        else:
            try:
                view[:] = self._i2c.write_read(address, data, len(view))
            except I2CError as error:
                raise OSError(str(error)) from error
