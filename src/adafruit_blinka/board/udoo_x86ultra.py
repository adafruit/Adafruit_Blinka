"""Pin definitions for Udoo x86 Ultra
(should work for Ultra and Ultra II)

There are 2 naming systems.  A Digital Pin system which includes
the arduino chip (Leonardo or 101).  The Braswell #s start at 16 and
is documented in the diagram and text for linux version later than 4.15 in:
https://www.udoo.org/docs-x86II/Introduction/Introduction.html
The other is based on the hardware manual:
https://udoo.org/download/files/UDOO_X86/Doc/UDOO_X86II_MANUAL.pdf

This will use the D system based on the diagram in the user guide

i2c use i2c(board.I2C0_SCL, board_I2C0_SDA) or i2c(board.I2C1_SCL, board_I2C1_SDA)
for the i2c(board.SCL, board.SCL) in the examples

UART use pyserial not busio
"""

from adafruit_blinka.microcontroller.pentium.n3710 import pin

# Connector CN15
D16 = pin.UART1_RTS
D17 = pin.UART1_CTS
D18 = pin.UART1_TXD
D19 = pin.UART1_RXD
D20 = pin.UART2_RTS
D21 = pin.UART2_CTS
D22 = pin.UART2_TXD
D23 = pin.UART2_RXD

# Connector CN13 LPC interface
D24 = pin.GPIO_275
D25 = pin.GPIO_280
D26 = pin.GPIO_273
D27 = pin.GPIO_278
D28 = pin.GPIO_276
D29 = pin.GPIO_279
D30 = pin.GPIO_307

# Connector CN14
D34 = pin.I2C0_SCL
D35 = pin.I2C0_SDA

D36 = pin.GPIO_492
D37 = pin.GPIO_490

D38 = pin.I2C1_SCL
D39 = pin.I2C1_SDA

# Connector CN12 SDIO SD/MMC interfaces
D40 = pin.GPIO_358
D41 = pin.GPIO_243
D42 = pin.GPIO_249
D43 = pin.GPIO_246
D44 = pin.GPIO_253
D45 = pin.GPIO_250
D46 = pin.GPIO_247

# aliases
UART1_RX = D19
UART1_TX = D18

UART2_RX = D23
UART2_TX = D22

I2C0_SCL = D34  # labeled on diagram as I2C1, hardware manual port 0
I2C0_SDA = D35  # i2cdetect-l lists it as i2c-0

I2C1_SCL = D38  # Labeled on diagram as I2C2, hardware manual port 5
I2C1_SCL = D39  # i2cdetect lists it as i2c-1
