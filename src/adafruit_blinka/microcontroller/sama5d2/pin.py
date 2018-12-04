from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PD23 = Pin(119)
PD21 = Pin(117)
PD20 = Pin(116)
PD24 = Pin(120)
PD22 = Pin(118)
PD19 = Pin(115)

SPI0_SCLK = Pin(14)
SPI0_MOSI = Pin(15)
SPI0_MISO = Pin(16)

UART1_RX = Pin(98)
UART1_TX = Pin(99)

PD13 = Pin(109)
PD31 = Pin(128)
PB0 = Pin(32)
PB7 = Pin(38)
PB1 = Pin(33)
PB5 = Pin(37)
PB3 = Pin(35)
TWI0_SCL = Pin(64)
TWI0_SDA = Pin(63)

i2cPorts = ( (0, TWI0_SCL, TWI0_SDA), )
# ordered as spiId, sckId, mosiId, misoId
spiPorts = ( (0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO), )
# ordered as uartId, txId, rxId
uartPorts = ( (1, UART1_TX, UART1_RX), )
