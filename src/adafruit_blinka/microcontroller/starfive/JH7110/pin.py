# SPDX-FileCopyrightText: 2024 Vladimir Shtarev, Jetbrains Research
#
# SPDX-License-Identifier: MIT
"""A Pin class for use with StarFive JH7110."""

import VisionFive.gpio as GPIO

GPIO.setmode(GPIO.BOARD)


class Pin:
    """Pins don't exist in CPython so...lets make our own!"""

    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2

    id = None
    _value = LOW
    _mode = IN

    def __init__(self, number):
        self.id = number

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        print(self.id)
        if mode is not None:
            if mode == self.IN:
                self._mode = self.IN
                GPIO.setup(self.id, GPIO.IN)
            elif mode == self.OUT:
                self._mode = self.OUT
                GPIO.setup(self.id, GPIO.OUT)
            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)
        if pull is not None:
            if self._mode != self.IN:
                raise RuntimeError("Cannot set pull resistor on output")
            if pull == self.PULL_UP:
                GPIO.setup(self.id, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            elif pull == self.PULL_DOWN:
                GPIO.setup(self.id, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            else:
                raise RuntimeError("Invalid pull for pin: %s" % self.id)

    def value(self, val=None):
        """Set or return the Pin Value"""
        if val is not None:
            if val == self.LOW:
                self._value = val
                GPIO.output(self.id, val)
            elif val == self.HIGH:
                self._value = val
                GPIO.output(self.id, val)
            else:
                raise RuntimeError("Invalid value for pin")
            return None
        return GPIO.input(self.id)


D7 = Pin(7)
D11 = Pin(11)
D12 = Pin(12)
D13 = Pin(13)
D15 = Pin(15)
D16 = Pin(16)
D18 = Pin(18)
D22 = Pin(22)
D24 = Pin(24)
D26 = Pin(26)
D27 = Pin(27)
D28 = Pin(28)
D29 = Pin(29)
D31 = Pin(31)
D35 = Pin(35)
D36 = Pin(36)
D37 = Pin(37)
D38 = Pin(38)
D40 = Pin(40)
# I2C
I2C_SDA = Pin(3)
I2C_SCL = Pin(5)

# SPI
SPI_MISO = Pin(21)
SPI_MOSI = Pin(19)
SPI_SCLK = Pin(23)

# UART
UART_TX = Pin(8)
UART_RX = Pin(10)

# PWM, does not support pwmio
PWM1 = Pin(32)
PWM2 = Pin(33)

# ordered as i2cId, SCL, SDA
i2cPorts = ((0, I2C_SCL, I2C_SDA),)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI_SCLK, SPI_MOSI, SPI_MISO),)

# ordered as uartId, txId, rxId
uartPorts = ((0, UART_TX, UART_RX),)
