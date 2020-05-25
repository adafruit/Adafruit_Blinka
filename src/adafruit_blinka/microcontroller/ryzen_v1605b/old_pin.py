"""UDOO Bolt pin names"""

from adafruit_blinka.microcontroller.generic_linux.sysfs_pin import Pin

# SPI_MISO = Pin(1)
# SPI_CS = Pin(2)
# SPI_MOSI = Pin(3)
# SPI_SCLK = Pin(4)
SCL2 = Pin(7)
SCL = Pin(8)
SDA2 = Pin(9)
SDA = Pin(10)
FAN_OUT = Pin(11)
FAN_TACH = Pin(12)
KSO0 = Pin(13)
KSI0 = Pin(14)
KSO1 = Pin(15)
KSI1 = Pin(16)
KSO2 = Pin(17)
KSI2 = Pin(18)
KSO3 = Pin(19)
KSI3 = Pin(20)
KSO4 = Pin(21)
KSI4 = Pin(22)
KSO8 = Pin(23)
KSO11 = Pin(24)
KSO9 = Pin(25)
KSO12 = Pin(26)
KSO10 = Pin(27)
KSO13 = Pin(28)
UART2_RX = Pin(33)
UART1_RX = Pin(34)
UART2_TX = Pin(35)
UART1_TX = Pin(36)
UART2_RTS = Pin(37)
UART1_RTS = Pin(38)
UART2_CTS = Pin(39)
UART1_CTS = Pin(40)

# ordered as i2cid, scl, sda
i2cPorts = (
    (0, SCL, SDA),
    (1, SCL2, SDA2),
)

# ordered as spiId, sckId, mosiId, misoId
# spiPorts = ((0, SPI_SCLK, SPI_MOSI, SPI_MISO),)
# spiPorts = ()

# ordered as uartId, txId, rxId
uartPorts = (
    (0, UART1_TX, UART1_RX),
    (1, UART2_TX, UART2_RX),
)
