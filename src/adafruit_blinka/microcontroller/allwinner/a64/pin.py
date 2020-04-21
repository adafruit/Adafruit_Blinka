"""Allwinner A64 pin names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PB0 = Pin((1, 32))
UART2_TX = PB0
PB1 = Pin((1, 33))
UART2_RX = PB1
PB2 = Pin((1, 34))
PB3 = Pin((1, 35))
PB4 = Pin((1, 36))
PB5 = Pin((1, 37))
PB6 = Pin((1, 38))
PB7 = Pin((1, 39))

PC0 = Pin((1, 64))
SPI0_MOSI = PC0
PC1 = Pin((1, 65))
SPI0_MISO = PC1
PC2 = Pin((1, 66))
SPI0_SCLK = PC2
PC3 = Pin((1, 67))
SPI0_CS = PC3
PC4 = Pin((1, 68))
PC5 = Pin((1, 69))
PC6 = Pin((1, 70))
PC7 = Pin((1, 71))
PC8 = Pin((1, 72))
PC9 = Pin((1, 73))
PC10 = Pin((1, 74))
PC11 = Pin((1, 75))
PC12 = Pin((1, 76))
PC13 = Pin((1, 77))
PC14 = Pin((1, 78))
PC15 = Pin((1, 79))
PC16 = Pin((1, 80))

PD0 = Pin((1, 96))
UART3_TX = PD0
SPI1_CS = PD0
PD1 = Pin((1, 97))
SPI1_SCLK = PD1
UART3_RX = PD1
PD2 = Pin((1, 98))
UART4_TX = PD2
SPI1_MOSI = PD2
PD3 = Pin((1, 99))
UART4_RX = PD3
SPI1_MISO = PD3
PD4 = Pin((1, 100))
PD5 = Pin((1, 101))
PD6 = Pin((1, 102))

PE14 = Pin((1, 142))
TWI2_SCL = PE14
PE15 = Pin((1, 143))
TWI2_SDA = PE15

PH2 = Pin((1, 226))
TWI1_SCL = PH2
PH3 = Pin((1, 227))
TWI1_SDA = PH3
PH4 = Pin((1, 228))
PH5 = Pin((1, 229))
PH6 = Pin((1, 230))
PH7 = Pin((1, 231))
PH8 = Pin((1, 232))
PH9 = Pin((1, 233))

PL2 = Pin((0, 2))
PL3 = Pin((0, 3))
PL8 = Pin((0, 8))
PL9 = Pin((0, 9))
PL10 = Pin((0, 10))

# ordered as i2cId, sclId, sdaId
i2cPorts = ((1, TWI1_SCL, TWI1_SDA), (2, TWI2_SCL, TWI2_SDA))

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),
    (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),
)
# ordered as uartId, txId, rxId
uartPorts = (
    (2, UART2_TX, UART2_RX),
    (3, UART3_TX, UART3_RX),
    (4, UART4_TX, UART4_RX),
)
