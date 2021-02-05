"""Pin definitions for the NanoPi Duo2."""
# Enable I2C0, UART1, and SPI by adding the following lines to /boot/armbianEnv.txt
#    overlays=usbhost2 usbhost3 spi-spidev uart1 i2c0
#    param_spidev_spi_bus=0

from adafruit_blinka.microcontroller.allwinner.h3 import pin

# Left GPIO
PG11 = pin.PG11

# I2C
SDA = pin.PA12
SCL = pin.PA11

# SPI
SCLK = pin.PA14
MOSI = pin.PA15
MISO = pin.PA16
CE0 = pin.PA13

# Serial UART
UART1_TX = pin.PG6
UART1_RX = pin.PG7
