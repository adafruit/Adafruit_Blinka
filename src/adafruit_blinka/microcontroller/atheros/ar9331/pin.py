"""Atheros AR9331 pin names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

GPIO_0 = Pin((0, 0))
GPIO_1 = Pin((0, 1))
GPIO_2 = Pin((0, 2))
GPIO_3 = Pin((0, 3))
SPI_CLK = GPIO_3
GPIO_4 = Pin((0, 4))
SPI_MOSI = GPIO_4
GPIO_5 = Pin((0, 5))
SPI_MISO = GPIO_5
GPIO_6 = Pin((0, 6))
GPIO_7 = Pin((0, 7))
GPIO_8 = Pin((0, 8))
GPIO_9 = Pin((0, 9))
UART0_RX = GPIO_9
GPIO_10 = Pin((0, 10))
UART0_TX = GPIO_10
GPIO_11 = Pin((0, 11))
GPIO_12 = Pin((0, 12))
GPIO_13 = Pin((0, 13))
GPIO_14 = Pin((0, 14))
GPIO_15 = Pin((0, 15))
GPIO_16 = Pin((0, 16))
GPIO_17 = Pin((0, 17))
GPIO_18 = Pin((0, 18))
GPIO_19 = Pin((0, 19))
GPIO_20 = Pin((0, 20))
TWI0_SCL = GPIO_20

GPIO_21 = Pin((0, 21))
TWI0_SDA = GPIO_21
GPIO_22 = Pin((0, 22))
GPIO_23 = Pin((0, 23))
GPIO_24 = Pin((0, 24))
GPIO_25 = Pin((0, 25))
GPIO_26 = Pin((0, 26))
GPIO_27 = Pin((0, 27))
GPIO_28 = Pin((0, 28))

# ordered as i2cId, sclId, sdaId
i2cPorts = (0, TWI0_SCL, TWI0_SDA)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((1, SPI_CLK, SPI_MOSI, SPI_MISO),)

# ordered as uartId, txId, rxId
uartPorts = (0, UART0_TX, UART0_RX)
