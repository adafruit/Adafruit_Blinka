"""FT2232H pin names"""

from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.pin import Pin

# See https://eblot.github.io/pyftdi/pinout.html for detailed FTDI device pinout information

# MPSSE Port A
AD4 = Pin(4, interface_id=0)
AD5 = Pin(5, interface_id=0)
AD6 = Pin(6, interface_id=0)
AD7 = Pin(7, interface_id=0)
AC0 = Pin(8, interface_id=0)
AC1 = Pin(9, interface_id=0)
AC2 = Pin(10, interface_id=0)
AC3 = Pin(11, interface_id=0)
AC4 = Pin(12, interface_id=0)
AC5 = Pin(13, interface_id=0)
AC6 = Pin(14, interface_id=0)
AC7 = Pin(15, interface_id=0)

SCL0 = Pin(interface_id=0)
SDA0 = Pin(interface_id=0)
SCK0 = SCLK0 = Pin(interface_id=0)
MOSI0 = Pin(interface_id=0)
MISO0 = Pin(interface_id=0)

# MPSSE Port B
BD4 = Pin(4, interface_id=1)
BD5 = Pin(5, interface_id=1)
BD6 = Pin(6, interface_id=1)
BD7 = Pin(7, interface_id=1)
BC0 = Pin(8, interface_id=1)
BC1 = Pin(9, interface_id=1)
BC2 = Pin(10, interface_id=1)
BC3 = Pin(11, interface_id=1)
BC4 = Pin(12, interface_id=1)
BC5 = Pin(13, interface_id=1)
BC6 = Pin(14, interface_id=1)
BC7 = Pin(15, interface_id=1)

SCL1 = Pin(interface_id=1)
SDA1 = Pin(interface_id=1)
SCK1 = SCLK1 = Pin(interface_id=1)
MOSI1 = Pin(interface_id=1)
MISO1 = Pin(interface_id=1)

i2cPorts = (
    (0, SCL0, SDA0),
    (1, SCL1, SDA1),
)

spiPorts = (
    (0, SCLK0, MOSI0, MISO0),
    (1, SCLK1, MOSI1, MISO1),
)
