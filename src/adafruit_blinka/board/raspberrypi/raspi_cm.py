"""Pin definitions for Raspberry Pi Compute Modules."""

from adafruit_blinka.microcontroller.bcm283x import pin

D2 = pin.D2
SDA = pin.SDA
D3 = pin.D3
SCL = pin.SCL

D4 = pin.D4
D5 = pin.D5
D6 = pin.D6

D7 = pin.D7
CE1 = pin.D7
D8 = pin.D8
CE0 = pin.D8
D9 = pin.D9
MISO = pin.D9
D10 = pin.D10
MOSI = pin.D10
D11 = pin.D11
SCLK = pin.D11
SCK = pin.D11

D12 = pin.D12
D13 = pin.D13

D14 = pin.D14
TXD = pin.D14
D15 = pin.D15
RXD = pin.D15
# create alias for most of the examples
TX = pin.D14
RX = pin.D15

D16 = pin.D16
D17 = pin.D17
D18 = pin.D18
D19 = pin.D19
MISO_1 = pin.D19
D20 = pin.D20
MOSI_1 = pin.D20
D21 = pin.D21
SCLK_1 = pin.D21
SCK_1 = pin.D21
D22 = pin.D22
D23 = pin.D23
D24 = pin.D24
D25 = pin.D25
D26 = pin.D26
D27 = pin.D27
D28 = pin.D28
D29 = pin.D29
D30 = pin.D30
D31 = pin.D31
D32 = pin.D32
D33 = pin.D33
D34 = pin.D34
D35 = pin.D35
D36 = pin.D36
D37 = pin.D37
D38 = pin.D38
D39 = pin.D39
D40 = pin.D40
MISO_2 = pin.D40
D41 = pin.D41
MOSI_2 = pin.D41
D42 = pin.D42
SCLK_2 = pin.D42
SCK_2 = pin.D43
D43 = pin.D43
D44 = pin.D44
D45 = pin.D45

# Fake pin numbers to explicitly reference I2C bus devices (/dev/i2c-n) that may
# or may not be backed by specific physical pins (like virtual i2c buses from i2c-mux)
# eg: to reference i2c bus 5 (/dev/i2c-5), use SCL5 and SDA5
SDA0 = pin.SDA0
SDA1 = pin.SDA1
SDA2 = pin.SDA2
SDA3 = pin.SDA3
SDA4 = pin.SDA4
SDA5 = pin.SDA5
SDA6 = pin.SDA6
SDA7 = pin.SDA7
SDA8 = pin.SDA8
SDA9 = pin.SDA9
SDA10 = pin.SDA10
SDA11 = pin.SDA11
SCL0 = pin.SCL0
SCL1 = pin.SCL1
SCL2 = pin.SCL2
SCL3 = pin.SCL3
SCL4 = pin.SCL4
SCL5 = pin.SCL5
SCL6 = pin.SCL6
SCL7 = pin.SCL7
SCL8 = pin.SCL8
SCL9 = pin.SCL9
SCL10 = pin.SCL10
SCL11 = pin.SCL11
