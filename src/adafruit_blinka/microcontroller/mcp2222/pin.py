# SPDX-FileCopyrightText: 2026 Limor Fried for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""MCP2222 GPIO pins."""

from pymcp2222 import (
    IODirection,
    IOPinConfig,
    IO0Designation,
    IO1Designation,
    IO2Designation,
    IO3Designation,
    IO4Designation,
    IO5Designation,
)

from .mcp2222 import mcp2222

_GPIO = (
    IO0Designation.GPIO0,
    IO1Designation.GPIO1,
    IO2Designation.GPIO2,
    IO3Designation.GPIO3,
    IO4Designation.GPIO4,
    IO5Designation.GPIO5,
)


class Pin:
    """A GPIO pin with push-pull output and an optional input pull-up."""

    OUT = 0
    IN = 1
    OPEN_DRAIN = 2
    PULL_UP = 3
    LOW = 0
    HIGH = 1
    spi_active = False

    def __init__(self, pin_id=None):
        self.id = pin_id
        self._mode = None
        self._value = False

    def init(self, mode=IN, pull=None):
        """Configure this GPIO without changing the other pins."""
        if self.id == 4 and Pin.spi_active:
            raise RuntimeError("G4 is reserved while MCP2222 SPI is active")
        if self.id not in range(6):
            raise ValueError("Not an MCP2222 GPIO pin")
        if mode == self.OPEN_DRAIN:
            raise NotImplementedError("Open-drain output is not implemented")
        if mode not in (self.IN, self.OUT):
            raise ValueError("Unsupported pin mode")
        if pull is not None and (mode != self.IN or pull != self.PULL_UP):
            raise NotImplementedError("Only input pull-ups are supported")
        if mode == self.IN:
            config = IOPinConfig(
                _GPIO[self.id], IODirection.INPUT, pull_up=pull == self.PULL_UP
            )
        else:
            config = IOPinConfig(
                _GPIO[self.id],
                IODirection.OUTPUT,
                open_drain=False,
                idle_state=self._value,
            )
        mcp2222.io.set_config(self.id, config)
        self._mode = mode

    def value(self, val=None):
        """Read the pin level or set an output."""
        if self.id == 4 and Pin.spi_active:
            raise RuntimeError("G4 is reserved while MCP2222 SPI is active")
        if self._mode is None:
            raise RuntimeError("Pin is not initialized")
        if val is None:
            return mcp2222.io.gpio_read(self.id).value
        if self._mode == self.IN:
            raise AttributeError("Not an output")
        if val not in (self.LOW, self.HIGH):
            raise ValueError("Invalid pin value")
        mcp2222.io.gpio_write(self.id, val)
        self._value = bool(val)
        return None

    def deinit(self):
        """Return the GPIO to an input."""
        self.init()


G0 = Pin(0)
G1 = Pin(1)
G2 = Pin(2)
G3 = Pin(3)
G4 = Pin(4)
G5 = Pin(5)
SCL = Pin()
SDA = Pin()
SCK = SCLK = Pin()
MOSI = Pin()
MISO = Pin()
