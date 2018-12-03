from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PA0 = Pin(0)
PA1 = Pin(1)
PA2 = Pin(2)
PA3 = Pin(3)
PA6 = Pin(6)
PA7 = Pin(7)
PA8 = Pin(8)
PA9 = Pin(9)
PA10 = Pin(10)
PA11 = Pin(11)
TWI0_SCL = PA11
PA12 = Pin(12)
TWI0_SDA = PA12
PA13 = Pin(13)
UART3_TX = PA13
PA14 = Pin(14)
UART3_RX = PA14
PA18 = Pin(18)
PA19 = Pin(19)
PA20 = Pin(20)
PA21 = Pin(21)

PC0 = Pin(64)
SPI0_MOSI = PC0
PC1 = Pin(65)
SPI0_MISO = PC1
PC2 = Pin(66)
SPI0_SCLK = PC2
PC3 = Pin(67)
SPI0_CS = PC3
PC4 = Pin(68)
PC7 = Pin(71)

PD14 = Pin(110)

PG6 = Pin(198)
PG7 = Pin(199)
PG8 = Pin(200)
PG9 = Pin(201)

i2cPorts = ( (0, TWI0_SCL, TWI0_SDA), )
# ordered as spiId, sckId, mosiId, misoId
spiPorts = ( (0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO), )
# ordered as uartId, txId, rxId
uartPorts = ( (3, UART3_TX, UART3_RX), )
