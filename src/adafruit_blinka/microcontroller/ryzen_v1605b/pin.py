"""UDOO Bolt pin names"""

from adafruit_blinka.microcontroller.generic_linux.sysfs_pin import Pin

GPIO_112 = Pin(1)
# SPI_MISO = GPIO_112
GPIO_20 = Pin(2)
# SPI_CS = GPIO_20
GPIO_16 = Pin(3)
# SPI_MOSI = GPIO_16
GPIO_17 = Pin(4)
# SPI_SCLK = GPIO_17
GPIO_42 = Pin(7)
GPIO_21 = Pin(8)
GPIO_19 = Pin(9)
GPIO_1 = Pin(10)
GPIO_9 = Pin(11)
GPIO_3 = Pin(12)
GPIO_40 = Pin(13)
GPIO_150 = Pin(14)
GPIO_162 = Pin(15)
GPIO_160 = Pin(16)
GPIO_161 = Pin(17)
GPIO_158 = Pin(18)
GPIO_159 = Pin(19)
GPIO_92 = Pin(20)
GPIO_85 = Pin(21)
GPIO_123 = Pin(22)
GPIO_124 = Pin(23)
GPIO_125 = Pin(24)
GPIO_126 = Pin(25)
GPIO_127 = Pin(26)
GPIO_133 = Pin(27)
GPIO_134 = Pin(28)
GPIO_139 = Pin(33)
GPIO_140 = Pin(34)
GPIO_141 = Pin(35)
GPIO_142 = Pin(36)
GPIO_143 = Pin(37)
GPIO_54 = Pin(38)
GPIO_205 = Pin(39)
GPIO_32 = Pin(40)

# I2C
SCL = GPIO_21
SDA = GPIO_1

SCL2 = GPIO_42
SDA2 = GPIO_19

# ordered as i2cid, scl, sda
i2cPorts = (
    (0, SCL, SDA),
    (1, SCL2, SDA2),
)

# Fan
FAN_OUT = GPIO_9
FAN_TACH = GPIO_3

# Keyboard Scan Inputs
KSI0 = GPIO_150
KSI1 = GPIO_160
KSI2 = GPIO_158
KSI3 = GPIO_92
KSI4 = GPIO_123

# Keyboard Scan Outputs
KSO0 = GPIO_40
KSO1 = GPIO_162
KSO2 = GPIO_161
KSO3 = GPIO_159
KSO4 = GPIO_85
KSO8 = GPIO_124
KSO9 = GPIO_126
KSO10 = GPIO_133
KSO11 = GPIO_125
KSO12 = GPIO_127
KSO13 = GPIO_134

# ordered as spiId, sckId, mosiId, misoId
# spiPorts = ((0, SPI_SCLK, SPI_MOSI, SPI_MISO),)
# spiPorts = ()

# UARTs
UART1_RX = GPIO_140
UART1_TX = GPIO_142
UART1_CTS = GPIO_32
UART1_RTS = GPIO_54

UART2_RX = GPIO_139
UART2_TX = GPIO_141
UART2_CTS = GPIO_205
UART2_RTS = GPIO_143

# ordered as uartId, txId, rxId
uartPorts = (
    (0, UART1_TX, UART1_RX),
    (1, UART2_TX, UART2_RX),
)
