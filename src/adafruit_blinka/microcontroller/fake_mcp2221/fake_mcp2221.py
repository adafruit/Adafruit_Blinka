# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Chip Definition for MCP2221"""

import os
import time
import atexit

import hid


class MCP2221:
    """MCP2221 Device Class Definition"""

    def __init__(self):
        pass  # This is a "fake" implementation

    def close(self):
        """Close the hid device. Does nothing if the device is not open."""
        pass

    def __del__(self):
        # try to close the device before destroying the instance
        pass

    def _hid_xfer(self, report, response=True):
        """Perform HID Transfer"""
        return None

    # ----------------------------------------------------------------
    # MISC
    # ----------------------------------------------------------------
    def gp_get_mode(self, pin):
        """Get Current Pin Mode"""
        pass

    def gp_set_mode(self, pin, mode):
        """Set Current Pin Mode"""
        pass

    def _pretty_report(self, register):
        pass

    def _status_dump(self):
        pass

    def _sram_dump(self):
        pass

    def _reset(self):
        pass

    # ----------------------------------------------------------------
    # GPIO
    # ----------------------------------------------------------------
    def gpio_set_direction(self, pin, mode):
        """Set Current GPIO Pin Direction"""
        pass

    def gpio_set_pin(self, pin, value):
        """Set Current GPIO Pin Value"""
        pass

    def gpio_get_pin(self, pin):
        """Get Current GPIO Pin Value"""
        pass

    # ----------------------------------------------------------------
    # I2C
    # ----------------------------------------------------------------
    def _i2c_status(self):
        pass

    def _i2c_state(self):
        pass

    def _i2c_cancel(self):
        pass

    # pylint: disable=too-many-arguments,too-many-branches
    def _i2c_write(self, cmd, address, buffer, start=0, end=None):
        pass

    def _i2c_read(self, cmd, address, buffer, start=0, end=None):
        pass

    # pylint: enable=too-many-arguments
    def _i2c_configure(self, baudrate=100000):
        """Configure I2C"""
        pass

    def i2c_writeto(self, address, buffer, *, start=0, end=None):
        """Write data from the buffer to an address"""
        pass

    def i2c_readfrom_into(self, address, buffer, *, start=0, end=None):
        """Read data from an address and into the buffer"""
        pass

    def i2c_writeto_then_readfrom(
        self,
        address,
        out_buffer,
        in_buffer,
        *,
        out_start=0,
        out_end=None,
        in_start=0,
        in_end=None,
    ):
        """Write data from buffer_out to an address and then
        read data from an address and into buffer_in
        """
        pass

    def i2c_scan(self, *, start=0, end=0x79):
        """Perform an I2C Device Scan"""
        pass

    # ----------------------------------------------------------------
    # ADC
    # ----------------------------------------------------------------
    def adc_configure(self, vref=0):
        """Configure the Analog-to-Digital Converter"""
        pass

    def adc_read(self, pin):
        """Read from the Analog-to-Digital Converter"""
        pass

    # ----------------------------------------------------------------
    # DAC
    # ----------------------------------------------------------------
    def dac_configure(self, vref=0):
        """Configure the Digital-to-Analog Converter"""
        pass

    # pylint: disable=unused-argument
    def dac_write(self, pin, value):
        """Write to the Digital-to-Analog Converter"""
        pass

    # pylint: enable=unused-argument


mcp2221 = MCP2221()
