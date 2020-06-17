from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.pin import Pin

# See https://eblot.github.io/pyftdi/pinout.html for detailed FTDI device pinout information

# MPSSE Port A
AD4 = Pin(4, url="ftdi://ftdi:ft2232h/1")
AD5 = Pin(5, url="ftdi://ftdi:ft2232h/1")
AD6 = Pin(6, url="ftdi://ftdi:ft2232h/1")
AD7 = Pin(7, url="ftdi://ftdi:ft2232h/1")
AC0 = Pin(8, url="ftdi://ftdi:ft2232h/1")
AC1 = Pin(9, url="ftdi://ftdi:ft2232h/1")
AC2 = Pin(10, url="ftdi://ftdi:ft2232h/1")
AC3 = Pin(11, url="ftdi://ftdi:ft2232h/1")
AC4 = Pin(12, url="ftdi://ftdi:ft2232h/1")
AC5 = Pin(13, url="ftdi://ftdi:ft2232h/1")
AC6 = Pin(14, url="ftdi://ftdi:ft2232h/1")
AC7 = Pin(15, url="ftdi://ftdi:ft2232h/1")

SCL0 = Pin(url="ftdi://ftdi:ft2232h/1")
SDA0 = Pin(url="ftdi://ftdi:ft2232h/1")
SCK0 = SCLK0 = Pin(url="ftdi://ftdi:ft2232h/1")
MOSI0 = Pin(url="ftdi://ftdi:ft2232h/1")
MISO0 = Pin(url="ftdi://ftdi:ft2232h/1")

# MPSSE Port B
BD4 = Pin(4, url="ftdi://ftdi:ft2232h/2")
BD5 = Pin(5, url="ftdi://ftdi:ft2232h/2")
BD6 = Pin(6, url="ftdi://ftdi:ft2232h/2")
BD7 = Pin(7, url="ftdi://ftdi:ft2232h/2")
BC0 = Pin(8, url="ftdi://ftdi:ft2232h/2")
BC1 = Pin(9, url="ftdi://ftdi:ft2232h/2")
BC2 = Pin(10, url="ftdi://ftdi:ft2232h/2")
BC3 = Pin(11, url="ftdi://ftdi:ft2232h/2")
BC4 = Pin(12, url="ftdi://ftdi:ft2232h/2")
BC5 = Pin(13, url="ftdi://ftdi:ft2232h/2")
BC6 = Pin(14, url="ftdi://ftdi:ft2232h/2")
BC7 = Pin(15, url="ftdi://ftdi:ft2232h/2")

SCL1 = Pin(url="ftdi://ftdi:ft2232h/2")
SDA1 = Pin(url="ftdi://ftdi:ft2232h/2")
SCK1 = SCLK1 = Pin(url="ftdi://ftdi:ft2232h/2")
MOSI1 = Pin(url="ftdi://ftdi:ft2232h/2")
MISO1 = Pin(url="ftdi://ftdi:ft2232h/2")

i2cPorts = (
    (0, SCL0, SDA0),
    (1, SCL1, SDA1),
)

spiPorts = (
    (0, SCLK0, MOSI0, MISO0),
    (1, SCLK1, MOSI1, MISO1),
)
