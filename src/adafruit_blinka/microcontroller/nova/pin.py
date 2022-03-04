# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Binho Nova pin names"""


class Pin:
    """A basic Pin class for use with Binho Nova."""

    IN = "DIN"
    OUT = "DOUT"
    AIN = "AIN"
    AOUT = "AOUT"
    PWM = "PWM"
    LOW = 0
    HIGH = 1

    _nova = None

    def __init__(self, pin_id=None):
        if not Pin._nova:
            # pylint: disable=import-outside-toplevel
            from adafruit_blinka.microcontroller.nova import Connection

            # pylint: enable=import-outside-toplevel

            Pin._nova = Connection.getInstance()
        # check if pin is valid
        if pin_id > 4:
            raise ValueError("Invalid pin {}.".format(pin_id))

        self.id = pin_id

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        if self.id is None:
            raise RuntimeError("Can not init a None type pin.")
        # Nova does't have configurable internal pulls for
        if pull:
            raise ValueError("Internal pull up/down not currently supported.")
        Pin._nova.setIOpinMode(self.id, mode)

    def value(self, val=None):
        """Set or return the Pin Value"""
        if self.id is None:
            raise RuntimeError("Can not access a None type pin.")
        # read
        if val is None:
            return int(Pin._nova.getIOpinValue(self.id).split("VALUE ")[1])
        # write
        if val in (self.LOW, self.HIGH):
            Pin._nova.setIOpinValue(self.id, val)
            return None
        raise RuntimeError("Invalid value for pin")


# create pin instances for each pin
IO0 = Pin(0)
IO1 = Pin(1)
IO2 = Pin(2)
IO3 = Pin(3)
IO4 = Pin(4)

SCL = IO2
SDA = IO0
SCK = SCLK = IO3
MOSI = IO4
MISO = IO2
SS0 = IO0
SS1 = IO1

PWM0 = IO0
# No PWM support on IO1
PWM2 = IO2
PWM3 = IO3
PWM4 = IO4

# orderd as (channel, pin), id
pwmOuts = (((1, 0), PWM0), ((1, 2), PWM2), ((1, 3), PWM3), ((1, 4), PWM4))

UART1_TX = IO4
UART1_RX = IO3

# ordered as uartId, txId, rxId
uartPorts = ((0, UART1_TX, UART1_RX),)
