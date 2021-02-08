"""Allwinner H616 Pin Names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PC0 = Pin((1, 64))
SPI0_CLK = PC0
PC2 = Pin((1, 66))
SPI0_MOSI = PC2
PC3 = Pin((1, 67))
SPI0_CS0 = PC3
PC4 = Pin((1, 68))
SPI0_MISO = PC4
PC5  = Pin((1, 69))
PC6  = Pin((1, 70))
PC7 = Pin((1, 71))
PC8 = Pin((1, 72))
PC9 = Pin((1, 73))
PC10 = Pin((1, 74))
PC11 = Pin((1, 75))
PC14 = Pin((1, 78))
PC15 = Pin((1, 79))

PH2 = Pin((1, 226))
UART5_TX = PH2
PH3 = Pin((1, 227))
UART5_RX = PH3
PH4 = Pin((1, 228))
TWI3_SCL = PH4
PH5 = Pin((1, 229))
UART2_TX = PH5
TWI3_SDA = PH5
SPI1_CS0 = PH5
PH6 = Pin((1, 230))
UART2_RX = PH6
SPI1_CLK = PH6
PH7 = Pin((1, 231))
SPI1_MOSI = PH7
PH8 = Pin((1, 232))
SPI1_MISO = PH8
PH9 = Pin((1, 233))
SPI1_CS1 = PH9

i2cPorts = ((3, TWI3_SCL, TWI3_SDA),)
# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),
    (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),
)
# ordered as uartId, txId, rxId
uartPorts = (
    (2, UART2_TX, UART2_RX),
    (5, UART5_TX, UART5_RX),
)
