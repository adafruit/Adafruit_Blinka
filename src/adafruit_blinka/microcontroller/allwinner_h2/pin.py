from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PA0 = Pin(0)
UART2_TX = PA0
PA1 = Pin(1)
UART2_RX = PA1
PA2 = Pin(2)
PA3 = Pin(3)
PA6 = Pin(6)
PA10 = Pin(10)
PA11 = Pin(11)
TWI0_SCL = PA11
PA12 = Pin(12)
TWI0_SDA = PA12
PA13 = Pin(13)
PA14 = Pin(14)
SPI1_SCLK = PA14
PA15 = Pin(15)
SPI1_MOSI = PA15
PA16 = Pin(16)
SPI1_MISO = PA16
PA18 = Pin(18)
PA19 = Pin(19)

PG6 = Pin(198)
UART1_TX = PG6
PG7 = Pin(199)
UART1_RX = PG7

i2cPorts = ( (0, TWI0_SCL, TWI0_SDA), )
# ordered as spiId, sckId, mosiId, misoId
spiPorts = ( (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO), )
# ordered as uartId, txId, rxId
uartPorts = ( (2, UART2_TX, UART2_RX), )
