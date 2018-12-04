from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PD23 = Pin(119) #AD4
PD21 = Pin(117) #AD2
PD20 = Pin(116) #AD1
PD24 = Pin(120) #AD5
PD22 = Pin(118) #AD3
PD19 = Pin(115) #AD0

SPI0_SCLK = PA14
SPI0_MOSI = PA15
SPI0_MISO = PA16

UART1_RX = PD2
UART1_TX = PD3

PD13 = Pin(109)
PD31 = Pin(128)
PB0 = Pin(32)
PB7 = Pin(38)
PB1 = Pin(33)
PB5 = Pin(37)
PB3 = Pin(35)
TWI0_SCL = PC0
TWI0_SDA = PB31

i2cPorts = ( (0, TWI0_SCL, TWI0_SDA), )
# ordered as spiId, sckId, mosiId, misoId
spiPorts = ( (0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO), )
# ordered as uartId, txId, rxId
uartPorts = ( (3, UART1_TX, UART1_RX), )
