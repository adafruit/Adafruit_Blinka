from adafruit_blinka.microcontroller.amlogic.meson_g12_common.pin import *


I2C2_SDA = GPIO493
I2C2_SCL = GPIO494
I2C3_SDA = GPIO474
I2C3_SCL = GPIO475

UART1_TX = GPIO488
UART1_RX = GPIO489

SPI0_SCLK = GPIO487
SPI0_MISO = GPIO485
SPI0_MOSI = GPIO484

i2cPorts = ((2, I2C2_SCL, I2C2_SDA), (3, I2C3_SCL, I2C3_SDA), )
# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO), )
# ordered as uartId, txId, rxId
uartPorts = ((1, UART1_TX, UART1_RX), )
