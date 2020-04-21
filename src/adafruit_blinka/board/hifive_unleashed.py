"""Pin definitions for the Hifive Unleashed."""

from adafruit_blinka.microcontroller.hfu540 import pin

GPIO_A = pin.GPIO0
GPIO_B = pin.GPIO1
GPIO_C = pin.GPIO2
GPIO_D = pin.GPIO3
GPIO_E = pin.GPIO4
GPIO_F = pin.GPIO5
GPIO_G = pin.GPIO6
GPIO_H = pin.GPIO7
GPIO_I = pin.GPIO8
GPIO_J = pin.GPIO9
GPIO_K = pin.GPIO15

UART0_TXD = pin.UART0_TXD
UART0_RXD = pin.UART0_RXD
SPI0_SCLK = pin.SPI0_SCLK
SPI0_DIN = pin.SPI0_DIN
UART1_TXD = pin.UART1_TXD
SPI0_CS = pin.SPI0_CS
UART1_RXD = pin.UART1_RXD
SPI0_DOUT = pin.SPI0_DOUT
I2C0_SCL = pin.I2C0_SCL
I2C0_SDA = pin.I2C0_SDA

SDA = pin.I2C0_SDA
SCL = pin.I2C0_SCL

I2C0_SDA = pin.I2C0_SDA
I2C0_SCL = pin.I2C0_SCL

SCLK = pin.SPI0_SCLK
MOSI = pin.SPI0_DOUT
MISO = pin.SPI0_DIN
SPI_CS = pin.SPI0_CS
