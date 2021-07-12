"""
Pin definitions for the QT Py RP2040 with u2if firmware.

Adafruit CircuitPython 6.2.0 on 2021-04-05; Adafruit QTPy RP2040 with rp2040
>>> import board
>>> board.
A0              A1              A2              A3
BUTTON          D0              D1              D10
D2              D3              D4              D5
D6              D7              D8              D9
I2C             MISO            MOSI            NEOPIXEL
NEOPIXEL_POWER  RX              SCK             SCL
SCL1            SDA             SDA1            SPI
TX              UART
"""


from adafruit_blinka.microcontroller.rp2040_u2if import pin

D0 = pin.GP29
D1 = pin.GP28
D2 = pin.GP27
D3 = pin.GP26
D4 = pin.GP24
D5 = pin.GP25
D6 = pin.GP20
D7 = pin.GP5
D8 = pin.GP6
D9 = pin.GP4
D10 = pin.GP3

# A0 = pin.GP29 # not currently supported in firmware
A1 = pin.GP28
A2 = pin.GP27
A3 = pin.GP26

SCL = pin.GP25
SDA = pin.GP24

SCL1 = pin.GP23
SDA1 = pin.GP22

SCLK = SCK = pin.GP6
MOSI = pin.GP3
MISO = pin.GP4

NEOPIXEL = pin.GP12
NEOPIXEL_POWER = pin.GP11

BUTTON = pin.GP21

# access u2if via pin instance to open for specifc VID/PID
# pylint:disable = protected-access
pin.GP0._u2if_open_hid(0x239A, 0x00F7)
