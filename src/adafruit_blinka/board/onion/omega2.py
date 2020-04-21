"""Pin definitions for the Onion Omega2+ Expansion Dock."""

from adafruit_blinka.microcontroller.mips24kec import pin

D0 = pin.GPIO0
D1 = pin.GPIO1
D2 = pin.GPIO2
D3 = pin.GPIO3

D4 = pin.GPIO4
D5 = pin.GPIO5
D6 = pin.GPIO6
D7 = pin.GPIO7
D8 = pin.GPIO8
D9 = pin.GPIO9

D11 = pin.GPIO11
D15 = pin.GPIO15  # RGB LED Blue
D16 = pin.GPIO16  # RGB LED Green
D17 = pin.GPIO17  # RGB LED Red
D18 = pin.GPIO18
D19 = pin.GPIO19

SDA = pin.I2C0_SDA
SCL = pin.I2C0_SCL

SCLK = pin.SPI0_SCLK
MOSI = pin.SPI0_MOSI
MISO = pin.SPI0_MISO
CS = pin.SPI0_CS
SCK = SCLK

UART_TX = pin.UART1_TX
UART_RX = pin.UART1_RX
