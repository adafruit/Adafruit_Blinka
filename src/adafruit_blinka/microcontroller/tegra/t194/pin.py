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
SDA = Pin('DP_AUX_CH3_N')
SCL = Pin('DP_AUX_CH3_P')
SDA_1 = Pin('GEN2_I2C_SDA')
SCL_1 = Pin('GEN2_I2C_SCL')

Q06 = Pin('SOC_GPIO42')
AA03 = Pin('CAN0_DIN')
AA02 = Pin('CAN0_DOUT')
Z07 = Pin('SPI1_CS1_N')
Z06 = Pin('SPI1_CS0_N')
Z04 = Pin('SPI1_MISO')
Z05 = Pin('SPI1_MOSI')
Z03 = Pin('SPI1_SCK')
BB01 = Pin('CAN1_EN')
AA00 = Pin('CAN1_DOUT')
R05 = Pin('UART1_CTS')
R04 = Pin('UART1_RTS')
H07 = Pin('DAP2_SCLK')
I02 = Pin('DAP2_FS')
I01 = Pin('DAP2_DIN')
I00 = Pin('DAP2_DOUT')
N01 = Pin('SOC_GPIO54')
BB00 = Pin('CAN1_STB')
H00 = Pin('SOC_GPIO12')
Q01 = Pin('SOC_GPIO21')
AA01 = Pin('CAN1_DIN')
R00 = Pin('SOC_GPIO44')

i2cPorts = (
    (8, SCL, SDA), (1, SCL_1, SDA_1),
)
