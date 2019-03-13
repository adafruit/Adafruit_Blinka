import sys
import atexit
sys.path.append("/opt/nvidia/jetson-gpio/lib/python")
sys.path.append("/opt/nvidia/jetson-gpio/lib/python/Jetson/GPIO")
import Jetson.GPIO as GPIO
GPIO.setmode(GPIO.TEGRA_SOC)
GPIO.setwarnings(False)   # shh!

# Pins dont exist in CPython so...lets make our own!
class Pin:
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
        if mode != None:
            if mode == self.IN:
                self._mode = self.IN
                GPIO.setup(self.id, GPIO.IN)
            elif mode == self.OUT:
                self._mode = self.OUT
                GPIO.setup(self.id, GPIO.OUT)
            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)
        if pull != None:
            if self._mode != self.IN:
                raise RuntimeError("Cannot set pull resistor on output")
            if pull == self.PULL_UP:
                GPIO.setup(self.id, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            elif pull == self.PULL_DOWN:
                GPIO.setup(self.id, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            else:
                raise RuntimeError("Invalid pull for pin: %s" % self.id)

    def value(self, val=None):
        if val != None:
            if val == self.LOW:
                self._value = val
                GPIO.output(self.id, val)
            elif val == self.HIGH:
                self._value = val
                GPIO.output(self.id, val)
            else:
                raise RuntimeError("Invalid value for pin")
        else:
            return GPIO.input(self.id)

    @atexit.register
    def cleanup():
        print("Exiting... \nCleaning up pins")
        GPIO.cleanup()

# Cannot be used as GPIO
SDA = Pin('GEN2_I2C_SDA')
SCL = Pin('GEN2_I2C_SCL')
SDA_1 = Pin('GEN1_I2C_SDA')
SCL_1 = Pin('GEN1_I2C_SCL')

BB00 = Pin('AUD_MCLK')
S05 = Pin('CAM_AF_EN')
Z00 = Pin('GPIO_PZ0')
C04 = Pin('SPI1_CS1')
C03 = Pin('SPI1_CS0')
C01 = Pin('SPI1_MISO')
C00 = Pin('SPI1_MOSI')
C02 = Pin('SPI1_SCK')
V00 = Pin('LCD_BL_PW')
E06 = Pin('GPIO_PE6')
G03 = Pin('UART2_CTS')
G02 = Pin('UART2_RTS')
J07 = Pin('DAP4_SCLK')
J04 = Pin('DAP4_FS')
J05 = Pin('DAP4_DIN')
J06 = Pin('DAP4_DOUT')
Y02 = Pin('LCD_TE')
DD00 = Pin('SPI2_CS1')
B07 = Pin('SPI2_CS0')
B05 = Pin('SPI2_MISO')
B04 = Pin('SPI2_MOSI')
B06 = Pin('SPI2_SCK')

i2cPorts = (
    (1, SCL, SDA), (0, SCL_1, SDA_1),
)
