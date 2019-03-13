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
SDA = Pin('GPIO_SEN9')
SCL = Pin('GPIO_SEN8')
SDA_1 = Pin('GEN1_I2C_SDA')
SCL_1 = Pin('GEN1_I2C_SCL')

J04 = Pin('AUD_MCLK')
J06 = Pin('GPIO_AUD1')
AA02 = Pin('CAN_GPIO2')
N06 = Pin('GPIO_CAM7')
N04 = Pin('GPIO_CAM5')
N05 = Pin('GPIO_CAM6')
N03 = Pin('GPIO_CAM4')
AA01 = Pin('CAN_GPIO1')
I05 = Pin('GPIO_PQ5')
T03 = Pin('UART1_CTS')
T02 = Pin('UART1_RTS')
J00 = Pin('DAP1_SCLK')
J03 = Pin('DAP1_FS')
J02 = Pin('DAP1_DIN')
J01 = Pin('DAP1_DOUT')
P17 = Pin('GPIO_EXP_P17')
AA00 = Pin('CAN0_GPIO0')
Y01 = Pin('GPIO_MDM2')
P16 = Pin('GPIO_EXP_P16')
I04 = Pin('GPIO_PQ4')
J05 = Pin('GPIO_AUD0')

i2cPorts = (
    (1, SCL, SDA), (0, SCL_1, SDA_1),
)
