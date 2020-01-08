from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PB0 = Pin(32)
UART2_TX = PB0
PB1 = Pin(33)
UART2_RX = PB1
PB2 = Pin(34)
PB3 = Pin(35)
PB4 = Pin(36)
PB5 = Pin(37)
PB6 = Pin(38)
PB7 = Pin(39)

PC4 = Pin(68)

PD0 = Pin(96)
UART3_TX = PD0
SPI1_CS = PD0
PD1 = Pin(97)
SPI1_SCLK = PD1
UART3_RX = PD1
PD2 = Pin(98)
UART4_TX = PD2
SPI1_MOSI = PD2
PD3 = Pin(99)
UART4_RX = PD3
SPI1_MISO = PD3
PD4 = Pin(100)
PD5 = Pin(101)
PD6 = Pin(102)

PE14 = Pin(142)
TWI2_SCL = PE14
PE15 = Pin(143)
TWI2_SDA = PE15

PH2 = Pin(226)
TWI1_SCL = PH2
PH3 = Pin(227)
TWI1_SDA = PH3
PH4 = Pin(228)
PH5 = Pin(229)
PH6 = Pin(230)

PL2 = Pin(354)
PL3 = Pin(355)
PL9 = Pin(361)
PL10 = Pin(362)

# ordered as i2cId, sclId, sdaId
i2cPorts = (
    (1, TWI1_SCL, TWI1_SDA),
    (2, TWI2_SCL, TWI2_SDA)
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),
)
# ordered as uartId, txId, rxId
uartPorts = (
    (2, UART2_TX, UART2_RX),
    (3, UART3_TX, UART3_RX),
    (4, UART4_TX, UART4_RX),
)
