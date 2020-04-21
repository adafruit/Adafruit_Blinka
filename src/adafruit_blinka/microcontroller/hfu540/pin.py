"""Hifive Unleashed pin names"""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

UART0_TXD = Pin(5)
UART0_RXD = Pin(7)
SPI0_SCLK = Pin(8)
SPI0_DIN = Pin(10)
UART1_TXD = Pin(11)
SPI0_CS = Pin(12)
UART1_RXD = Pin(13)
SPI0_DOUT = Pin(14)
I2C0_SCL = Pin(15)
I2C0_SDA = Pin(17)
GPIO0 = Pin(23)
GPIO1 = Pin(24)
GPIO2 = Pin(25)
GPIO3 = Pin(26)
GPIO4 = Pin(27)
GPIO5 = Pin(28)
GPIO6 = Pin(29)
GPIO7 = Pin(30)
GPIO8 = Pin(31)
GPIO9 = Pin(32)
GPIO15 = Pin(33)

# ordered as spiId, sckId, mosiId, misoId
SPI_PORTS = (1, SPI0_SCLK, SPI0_DOUT, SPI0_DIN)

# ordered as uartId, txId, rxId
UART_PORTS = (
    (0, UART0_TXD, UART0_RXD),
    # (0, GPIO15, GPIO13)
    (1, UART1_TXD, UART1_RXD),
)

# ordered as i2cId, sclId, sdaId
I2C_PORTS = (0, I2C0_SDA, I2C0_SCL)
