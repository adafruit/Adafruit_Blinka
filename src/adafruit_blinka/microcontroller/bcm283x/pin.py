"""Broadcom BCM283x pin names"""
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # Use BCM pins D4 = GPIO #4
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
            elif val == self.HIGH:
                self._value = val
                GPIO.output(self.id, val)
            else:
                raise RuntimeError("Invalid value for pin")
            return None
        return GPIO.input(self.id)


# Pi 1B rev1 only?
D0 = Pin(0)
D1 = Pin(1)

D2 = Pin(2)
SDA = Pin(2)
D3 = Pin(3)
SCL = Pin(3)

D4 = Pin(4)
D5 = Pin(5)
D6 = Pin(6)

D7 = Pin(7)
CE1 = Pin(7)
D8 = Pin(8)
CE0 = Pin(8)
D9 = Pin(9)
MISO = Pin(9)
D10 = Pin(10)
MOSI = Pin(10)
D11 = Pin(11)
SCLK = Pin(11)  # Raspberry Pi naming
SCK = Pin(11)  # CircuitPython naming

D12 = Pin(12)
D13 = Pin(13)

D14 = Pin(14)
TXD = Pin(14)
D15 = Pin(15)
RXD = Pin(15)

D16 = Pin(16)
D17 = Pin(17)
D18 = Pin(18)
D19 = Pin(19)
MISO_1 = Pin(19)
D20 = Pin(20)
MOSI_1 = Pin(20)
D21 = Pin(21)
SCLK_1 = Pin(21)
SCK_1 = Pin(21)
D22 = Pin(22)
D23 = Pin(23)
D24 = Pin(24)
D25 = Pin(25)
D26 = Pin(26)
D27 = Pin(27)
D28 = Pin(28)
D29 = Pin(29)
D30 = Pin(30)
D31 = Pin(31)
D32 = Pin(32)
D33 = Pin(33)
D34 = Pin(34)
D35 = Pin(35)
D36 = Pin(36)
D37 = Pin(37)
D38 = Pin(38)
D39 = Pin(39)
D40 = Pin(40)
MISO_2 = Pin(40)
D41 = Pin(41)
MOSI_2 = Pin(41)
D42 = Pin(42)
SCLK_2 = Pin(42)
SCK_2 = Pin(43)
D43 = Pin(43)
D44 = Pin(44)
D45 = Pin(45)

# Let's use fake pin numbers in 5xx range to explicitly reference I2C bus devices (/dev/i2c-n) that
# may or may not be backed by specific physical pins (like virtual i2c buses from i2c-mux)
# eg: to reference i2c bus 5 (/dev/i2c-5), use SCL5 and SDA5
SDA0 = Pin(500)
SDA1 = Pin(501)
SDA2 = Pin(502)
SDA3 = Pin(503)
SDA4 = Pin(504)
SDA5 = Pin(505)
SDA6 = Pin(506)
SDA7 = Pin(507)
SDA8 = Pin(508)
SDA9 = Pin(509)
SDA10 = Pin(510)
SDA11 = Pin(511)
SCL0 = Pin(550)
SCL1 = Pin(551)
SCL2 = Pin(552)
SCL3 = Pin(553)
SCL4 = Pin(554)
SCL5 = Pin(555)
SCL6 = Pin(556)
SCL7 = Pin(557)
SCL8 = Pin(558)
SCL9 = Pin(559)
SCL10 = Pin(560)
SCL11 = Pin(561)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SCLK, MOSI, MISO),
    (1, SCLK_1, MOSI_1, MISO_1),
    (2, SCLK_2, MOSI_2, MISO_2),
)

# ordered as uartId, txId, rxId
uartPorts = ((1, TXD, RXD),)

i2cPorts = (
    (11, SCL11, SDA11),
    (10, SCL10, SDA10),
    (9, SCL9, SDA9),
    (8, SCL8, SDA8),
    (7, SCL7, SDA7),
    (6, SCL6, SDA6),
    (5, SCL5, SDA5),
    (4, SCL4, SDA4),
    (3, SCL3, SDA3),
    (2, SCL2, SDA2),
    (1, SCL1, SDA1),
    (0, SCL0, SDA0),
    (1, SCL, SDA),
    (0, D1, D0),  # both pi 1 and pi 2 i2c ports!
)
