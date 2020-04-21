from adafruit_blinka.microcontroller.amlogic.meson_g12_common.pin import *


I2C1_SDA = GPIOX_17
I2C1_SCL = GPIOX_18
I2C2_SDA = GPIOA_14
I2C2_SCL = GPIOA_15

UART1_TX = GPIOX_12
UART1_RX = GPIOX_13

SPI0_SCLK = GPIOX_11
SPI0_MISO = GPIOX_9
SPI0_MOSI = GPIOX_8
SPI0_CS0 = GPIOX_10

i2cPorts = ((1, I2C1_SCL, I2C1_SDA), (2, I2C2_SCL, I2C2_SDA), )
# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO), )
# ordered as uartId, txId, rxId
uartPorts = ((1, UART1_TX, UART1_RX), )
