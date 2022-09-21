# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: 2022 Martin Schnur for Siemens AG
#
# SPDX-License-Identifier: MIT
"""TI AM65XX pin names"""

import mraa

# pylint: disable=too-many-branches,too-many-statements
# pylint: disable=pointless-string-statement


class Pin:
    """Pins don't exist in CPython so...lets make our own!"""

    # pin modes
    IN = 0
    OUT = 1
    ADC = 2
    DAC = 3
    PWM = 4
    # pin values
    LOW = 0
    HIGH = 1
    # pin pulls
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2

    id = None
    _value = LOW
    _mode = IN

    def __init__(self, pin_id=None):
        self.id = pin_id
        self._mode = None
        self._pull = None
        self._pin = None

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        if self.id is None:
            raise RuntimeError("Can not init a None type pin.")
        if mode is not None:
            if mode == self.IN:
                self._mode = self.IN
                mypin = mraa.Gpio(self.id)
                mypin.dir(mraa.DIR_IN)
            elif mode == self.OUT:
                self._mode = self.OUT
                mypin = mraa.Gpio(self.id)
                mypin.dir(mraa.DIR_OUT)
            elif mode in (self.ADC, self.DAC):
                # ADC (DAC not available) only available on Pin 0-5 (X12 Pin 1-6)
                if self.id not in (0, 1, 2, 3, 4, 5):
                    raise ValueError("Pin does not have ADC capabilities")
                self._pin = mraa.Aio(self.id)
            elif mode == self.PWM:
                # PWM only available on Pin 4-9 (X10 Pin 1-2, X11 Pin 5-8)
                if self.id not in (4, 5, 6, 7, 8, 9):
                    raise ValueError("Pin does not have PWM capabilities")
                return
            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)
            self._mode = mode
        if pull is not None:
            if self._mode != self.IN:
                raise RuntimeError("Cannot set pull resistor on output")
            if pull == self.PULL_UP:
                mypin = mraa.Gpio(self.id)
                mypin.dir(mraa.DIR_IN)
            elif pull == self.PULL_DOWN:
                mypin = mraa.Gpio(self.id)
                mypin.dir(mraa.DIR_IN)
            else:
                raise RuntimeError("Invalid pull for pin: %s" % self.id)

    def value(self, val=None):
        """Set or return the Pin Value"""
        # Digital In / Out
        if self._mode in (Pin.IN, Pin.OUT):
            if val is not None:
                if val == self.LOW:
                    self._value = val
                    mypin = mraa.Gpio(self.id)
                    mypin.write(0)
                elif val == self.HIGH:
                    self._value = val
                    mypin = mraa.Gpio(self.id)
                    mypin.write(1)
                else:
                    raise RuntimeError("Invalid value for pin")
                return None
            return mraa.Gpio.read(mraa.Gpio(self.id))
        # Analog In
        if self._mode == Pin.ADC:
            if val is None:
                # Read ADC here
                mypin = mraa.Aio(self.id)
                mypin.read()
                return mypin.read()
            # read only
            raise AttributeError("'AnalogIn' object has no attribute 'value'")
        # Analog Out
        if self._mode == Pin.DAC:
            """if val is None:
                # write only
                raise AttributeError("unreadable attribute")
            # Set DAC here
            mypin = mraa.Aio(self.id)
            mypin.setBit(val)"""
            raise AttributeError(
                "AM65xx doesn't have an DAC! No Analog Output possible!"
            )
        raise RuntimeError(
            "No action for mode {} with value {}".format(self._mode, val)
        )


# Digital Pins (GPIO 0-19)
D0 = Pin(0)
D1 = Pin(1)
D2 = Pin(2)
D3 = Pin(3)
D4 = Pin(4)
D5 = Pin(5)
D6 = Pin(6)
D7 = Pin(7)
D8 = Pin(8)
D9 = Pin(9)
D10 = Pin(10)
D11 = Pin(11)
D12 = Pin(12)
D13 = Pin(13)
D14 = Pin(14)
D15 = Pin(15)
D16 = Pin(16)
D17 = Pin(17)
D18 = Pin(18)
D19 = Pin(19)

# Analog Pins (AIO 0-5, only ADC!)
A0 = Pin(0)
A1 = Pin(1)
A2 = Pin(2)
A3 = Pin(3)
A4 = Pin(4)
A5 = Pin(5)

# I2C allocation
I2C_SCL = "SCL"
I2C_SDA = "SDA"

# SPI allocation
SPIO_SCLK = D13
SPIO_MISO = D12
SPIO_MOSI = D11
SPIO_SS = D10

# UART allocation
UART_TX = "TX"
UART_RX = "RX"

# pwmOuts (GPIO 4-9)
PWM_4 = D4
PWM_5 = D5
PWM_6 = D6
PWM_7 = D7
PWM_8 = D8
PWM_9 = D9

# I2C
# ordered as sclID, sdaID
# i2c-4 (/dev/i2c-4) -> X10 Pin9, Pin10 (SDA, SCL)
i2cPorts = ((4, I2C_SCL, I2C_SDA),)

# SPI
# ordered as spiId, sckId, mosiID, misoID
spiPorts = ((0, SPIO_SCLK, SPIO_MOSI, SPIO_MISO),)

# UART
# use pySerial = dev/ttyS1
# ordered as uartID, txID, rxID
uartPorts = ((0, UART_TX, UART_RX),)

# PWM
pwmOuts = (
    ((0, 0), PWM_4),
    ((0, 1), PWM_5),
    ((2, 0), PWM_6),
    ((2, 1), PWM_7),
    ((4, 0), PWM_8),
    ((4, 1), PWM_9),
)
