# SPDX-FileCopyrightText: 2025 Gautham Srinivasan for NVIDIA
#
# SPDX-License-Identifier: MIT

"""Tegra T264 pin names"""
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
SDA = Pin("GP16_I2C8_DAT")  # I2C4
SCL = Pin("GP81_I2C9_CLK")
SDA_1 = Pin("GP14_I2C2_DAT")  # I2C2
SCL_1 = Pin("GP13_I2C2_CLK")

# Jetson Thor
L06 = Pin("GP130")
M04 = Pin("GP136_UART9_RTS_N")
V06 = Pin("GP184_DAP2_CLK")
M00 = Pin("GP132_PWM9")
F07 = Pin("GP257_PWM2")
DD03 = Pin("GP21")
U07 = Pin("GP177")
K01 = Pin("GP117_SPI1_MOSI")
K00 = Pin("GP116_SPI1_MISO")
U00 = Pin("GP170")
J07 = Pin("GP115_SPI1_CLK")
K02 = Pin("GP118_SPI1_CS0_N")
K03 = Pin("GP119_SPI1_CS1_N")
AD01 = Pin("GP211_CAN2_DIN")
AD00 = Pin("GP210_CAN2_DOUT")
DD04 = Pin("GGP22_SOCKET_ID_STRA")
AE00 = Pin("GP215_CAN3_DOUT")
W01 = Pin("GP187_DAP2_FS")
M05 = Pin("GP137_UART9_CTS_N")
AE01 = Pin("GP216_CAN3_DIN")
W00 = Pin("GP186_DAP2_DIN")
V07 = Pin("GP185_DAP2_DOUT")

i2cPorts = (
    (7, SCL, SDA),
    (1, SCL_1, SDA_1),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((K02, J07, K01, K00),)
