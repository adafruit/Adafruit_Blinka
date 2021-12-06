"""Pin definitions for the Octavo OSD32MP1 RED board."""

from adafruit_blinka.microcontroller.stm32.stm32mp157 import pin

# RPi header JP20
D0 = pin.PF15
D1 = pin.PD12
D2 = pin.PA12
D3 = pin.PA11
D4 = pin.PI11
D5 = pin.PG2
D6 = pin.PH11
D7 = pin.PF13
D8 = pin.PF6
D9 = pin.PF8
D10 = pin.PF9
D11 = pin.PF7
D12 = pin.PD13
D13 = pin.PB5
D14 = pin.PB10
D15 = pin.PB12
D16 = pin.PB13
D17 = pin.PG8
D18 = pin.PI5
D19 = pin.PI7
D20 = pin.PI6
D21 = pin.PE11
D22 = pin.PG15
D23 = pin.PF1
D24 = pin.PF0
D25 = pin.PF4
D26 = pin.PF5
D27 = pin.PD7

I2C5_SDA = SDA = D2
I2C5_SCL = SCL = D3

I2C1_SDA = ID_SD = D0
I2C1_SCL = ID_SC = D1

SPI5_SCLK = SCLK = SCK = D11
SPI5_MOSI = MOSI = D10
SPI5_MISO = MISO = D9
SPI5_NSS = CS = CE0 = D8

PI_GPIO7 = CE1 = D7

UART_TX = D14
UART_RX = D15

# Console UART
UART4_TX = pin.PG11
UART4_RX = pin.PB2
