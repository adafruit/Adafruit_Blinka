"""FT232H pin names"""

from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.pin import Pin

# See https://eblot.github.io/pyftdi/pinout.html for detailed FTDI device pinout information

# MPSSE Port A
D4 = Pin(4)
D5 = Pin(5)
D6 = Pin(6)
D7 = Pin(7)
C0 = Pin(8)
C1 = Pin(9)
C2 = Pin(10)
C3 = Pin(11)
C4 = Pin(12)
C5 = Pin(13)
C6 = Pin(14)
C7 = Pin(15)

SCL = Pin()
SDA = Pin()
SCK = SCLK = Pin()
MOSI = Pin()
MISO = Pin()
