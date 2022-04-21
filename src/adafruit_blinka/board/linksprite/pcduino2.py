"""Pin definitions for the Pcduino2."""
from adafruit_blinka.microcontroller.allwinner.a10 import pin

#J11 Header
D0 = pin.PI19
D1 = pin.PI18
D2 = pin.PH7
D3 = pin.PH6
D4 = pin.PH8
D5 = pin.PB2
D6 = pin.PI3
D7 = pin.PH9

#J8 Header
D8 = pin.PH10
D9 = pin.PH5
D10 = pin.PI10
D11 = pin.PI12
D12 = pin.PI13
D13 = pin.PI11
SDA2 = pin.PB21
SCL2 = pin.PB20

#P7 Header
SCLK = D13
MOSI = D11
MSIO = D12
CS = D10


#P6 Header
SCLK2 = pin.PC20
MOSI2 = pin.PC21
MSIO2 = pin.PC22
CS2 = pin.PC19

#P10 Header
D14 = pin.PH11
D15 = pin.PH12
D16 = pin.PH13
D17 = pin.PH14

UART2_TX = D1
UART2_RX = D0
UART5_TX = D3
UART5_RX = D2

#Misc
BACK_SW = pin.PH17 #Three buttons featured on the board
HOME_SW = pin.PH18
MENU_SW = pin.PH19