# SPDX-FileCopyrightText: 2022 Linh Hoang for NVIDIA
# SPDX-FileCopyrightText: 2022 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""Tegra T234 pin names"""
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

# Jetson AGX Orin
Q06 = Pin("GP66")
R04 = Pin("GP72_UART1_RTS_N")
H07 = Pin("GP122")
R00 = Pin("GP68")
N01 = Pin("GP88_PWM1")
BB00 = Pin("GP25")
H00 = Pin("GP115")
Z05 = Pin("GP49_SPI1_MOSI")
Z04 = Pin("GP48_SPI1_MISO")
P04 = Pin("GP56")
Z03 = Pin("GP47_SPI1_CLK")
Z06 = Pin("GP50_SPI1_CS0_N")
Z07 = Pin("GP51_SPI1_CS1_N")
AA01 = Pin("GP18_CAN0_DIN")
AA00 = Pin("GP17_CAN0_DOUT")
BB01 = Pin("GP26")
AA02 = Pin("GP19_CAN1_DOUT")
I02 = Pin("GP125")
R05 = Pin("GP73_UART1_CTS_N")
AA03 = Pin("GP20_CAN1_DIN")
I01 = Pin("GP124")
I00 = Pin("GP123")


AC06 = Pin("GP167")
Y00 = Pin("SPI1_SCK")
N01 = Pin("GP88_PWM1")
Y04 = Pin("GP40_SPI3_CS1_N")
Y03 = Pin("GP39_SPI3_CS0_N")
Y01 = Pin("GP37_SPI3_MISO")
Q05 = Pin("GP65")
G06 = Pin("GP113_PWM7")
Y02 = Pin("GP38_SPI3_MOSI")


i2cPorts = (
    (7, SCL, SDA),
    (1, SCL_1, SDA_1),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, Z03, Z05, Z04),)
