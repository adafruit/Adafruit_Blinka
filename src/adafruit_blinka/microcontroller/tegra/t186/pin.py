# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Tegra T186 pin names"""

import atexit
from Jetson import GPIO

GPIO.setmode(GPIO.TEGRA_SOC)
GPIO.setwarnings(False)  # shh!


class Pin:
    """Pins dont exist in CPython so...lets make our own!"""

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

    def __init__(self, bcm_number):
        self.id = bcm_number

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
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
                return None
            if val == self.HIGH:
                self._value = val
                GPIO.output(self.id, val)
                return None
            raise RuntimeError("Invalid value for pin")
        return GPIO.input(self.id)

    # pylint: disable=no-method-argument
    @atexit.register
    def cleanup():
        """Clean up pins"""
        print("Exiting... \nCleaning up pins")
        GPIO.cleanup()

    # pylint: enable=no-method-argument


# Cannot be used as GPIO
SDA = Pin("GPIO_SEN9")
SCL = Pin("GPIO_SEN8")
SDA_1 = Pin("GEN1_I2C_SDA")
SCL_1 = Pin("GEN1_I2C_SCL")

# Jetson TX2 specific
J06 = Pin("GPIO_AUD1")
AA02 = Pin("CAN_GPIO2")
N06 = Pin("GPIO_CAM7")
N04 = Pin("GPIO_CAM5")
N05 = Pin("GPIO_CAM6")
N03 = Pin("GPIO_CAM4")
AA01 = Pin("CAN_GPIO1")
I05 = Pin("GPIO_PQ5")
T03 = Pin("UART1_CTS")
T02 = Pin("UART1_RTS")
P17 = Pin("GPIO_EXP_P17")
AA00 = Pin("CAN_GPIO0")
Y01 = Pin("GPIO_MDM2")
P16 = Pin("GPIO_EXP_P16")
I04 = Pin("GPIO_PQ4")
J05 = Pin("GPIO_AUD0")

# Jetson TX2 NX specific
W04 = Pin("UART3_RTS")
V01 = Pin("GPIO_SEN1")
C02 = Pin("DAP2_DOUT")
C03 = Pin("DAP2_DIN")
V04 = Pin("GPIO_SEN4")
H02 = Pin("GPIO_WAN7")
H01 = Pin("GPIO_WAN6")
V02 = Pin("GPIO_SEN2")
H00 = Pin("GPIO_WAN5")
H03 = Pin("GPIO_WAN8")
Y03 = Pin("GPIO_MDM4")
N01 = Pin("GPIO_CAM2")
EE02 = Pin("TOUCH_CLK")
U00 = Pin("GPIO_DIS0")
U05 = Pin("GPIO_DIS5")
W05 = Pin("UART3_CTS")
V03 = Pin("GPIO_SEN3")

# Shared pin
J03 = Pin("DAP1_FS")
J02 = Pin("DAP1_DIN")
J01 = Pin("DAP1_DOUT")
J00 = Pin("DAP1_SCLK")
J04 = Pin("AUD_MCLK")

i2cPorts = (
    (1, SCL, SDA),
    (0, SCL_1, SDA_1),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((3, N03, N05, N04),)
