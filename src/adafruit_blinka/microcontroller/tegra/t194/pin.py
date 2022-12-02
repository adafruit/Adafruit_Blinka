# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Tegra T194 pin names"""
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
SDA = Pin("DP_AUX_CH3_N")
SCL = Pin("DP_AUX_CH3_P")
SDA_1 = Pin("GEN2_I2C_SDA")
SCL_1 = Pin("GEN2_I2C_SCL")

# Jetson Xavier only
Q06 = Pin("SOC_GPIO42")
AA03 = Pin("CAN0_DIN")
AA02 = Pin("CAN0_DOUT")
BB01 = Pin("CAN1_EN")
AA00 = Pin("CAN1_DOUT")
H07 = Pin("DAP2_SCLK")
I02 = Pin("DAP2_FS")
I01 = Pin("DAP2_DIN")
I00 = Pin("DAP2_DOUT")
BB00 = Pin("CAN1_STB")
H00 = Pin("SOC_GPIO12")
Q01 = Pin("SOC_GPIO21")
AA01 = Pin("CAN1_DIN")

# Jetson NX only
S04 = Pin("AUD_MCLK")
T05 = Pin("DAP5_SCLK")
Y00 = Pin("SPI3_SCK")
CC04 = Pin("TOUCH_CLK")
Y04 = Pin("SPI3_CS1_N")
Y03 = Pin("SPI3_CS0_N")
Y01 = Pin("SPI3_MISO")
Q05 = Pin("SOC_GPIO41")
Q06 = Pin("SOC_GPIO42")
U00 = Pin("DAP5_FS")
Y02 = Pin("SPI3_MOSI")
T07 = Pin("DAP5_DIN")
T06 = Pin("DAP5_DOUT")

# Clara AGX Xavier only
P04 = Pin("SOC_GPIO04")

# Shared
N01 = Pin("SOC_GPIO54")
R00 = Pin("SOC_GPIO44")
R04 = Pin("UART1_RTS")
R05 = Pin("UART1_CTS")
Z03 = Pin("SPI1_SCK")
Z04 = Pin("SPI1_MISO")
Z05 = Pin("SPI1_MOSI")
Z06 = Pin("SPI1_CS0_N")
Z07 = Pin("SPI1_CS1_N")

i2cPorts = (
    (8, SCL, SDA),
    (1, SCL_1, SDA_1),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, Z03, Z05, Z04),)
