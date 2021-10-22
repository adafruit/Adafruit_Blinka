"""Broadcom BCM2711 pin names"""
import RPi.GPIO as GPIO
from adafruit_blinka.microcontroller.bcm283x.pin import Pin

GPIO.setmode(GPIO.BCM)  # Use BCM pins D4 = GPIO #4
GPIO.setwarnings(False)  # shh!

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

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SCLK, MOSI, MISO),
    (6, SCLK_1, MOSI_1, MISO_1),
    (2, SCLK_2, MOSI_2, MISO_2),
    (3, D3, D2, D1),
    (4, D7, D6, D5),
    (5, D15, D14, D13),
)

# ordered as uartId, txId, rxId
uartPorts = ((1, TXD, RXD),)

# These are the known hardware I2C ports / pins.
# For software I2C ports created with the i2c-gpio overlay, see:
#     https://github.com/adafruit/Adafruit_Python_Extended_Bus
i2cPorts = (
    (1, SCL, SDA),
    (0, D1, D0),  # both pi 1 and pi 2 i2c ports!
    (10, D45, D44),  # internal i2c bus for the CM4
)
