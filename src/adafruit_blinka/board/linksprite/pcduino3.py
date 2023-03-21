"""Pin definitions for the Pcduino3."""
from adafruit_blinka.microcontroller.allwinner.a20 import pin

# Pin wise this is the same as the Pcduino2 but features a daul core A20
# # rather than a single core A10

# J11 Header
D0 = pin.PI19
D1 = pin.PI18
D2 = pin.PH7
D3 = pin.PH6
D4 = pin.PH8
D5 = pin.PB2
D6 = pin.PI3
D7 = pin.PH9

# J8 Header
D8 = pin.PH10
D9 = pin.PH5
D10 = pin.PI10
D11 = pin.PI12
D12 = pin.PI13
D13 = pin.PI11
SDA = pin.PB21
SCL = pin.PB20

# J9 Header
# A0 & A1 are LRADC pins with only 6-bit resolution and unlike other pins are only limited to 2v
A2 = pin.XP_TP
A3 = pin.XN_TP
A4 = pin.YP_TP
A5 = pin.YN_TP

# P7 Header
SCLK = D13
SCK = SCLK
MOSI = D11
MISO = D12
CS = D10


# P6 Header
D22 = pin.PC20
SCLK2 = D22
SCK2 = SCLK2
D23 = pin.PC21
MOSI2 = D23
D20 = pin.PC22
MISO2 = D20
D21 = pin.PC19
CS2 = D21

# P10 Header
D14 = pin.PH11
D15 = pin.PH12
D16 = pin.PH13
D17 = pin.PH14

UART2_TX = D1
UART2_RX = D0
UART5_TX = D3
UART5_RX = D2

PWM0 = D5
PWM1 = D6

# Misc
BACK_SW = pin.PH17  # Three buttons featured on the board
HOME_SW = pin.PH18
MENU_SW = pin.PH19
