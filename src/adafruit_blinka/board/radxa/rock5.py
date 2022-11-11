"""Pin definitions for the Rock 5"""

from adafruit_blinka.microcontroller.rockchip.rk3588 import pin


D0 = pin.GPIO4_C6
D1 = pin.GPIO4_C5
D2 = pin.GPIO4_B3
D3 = pin.GPIO4_B2
D4 = pin.GPIO3_C3
D5 = pin.GPIO1_D7
D6 = pin.GPIO1_B7
D7 = pin.GPIO1_B5
D8 = pin.GPIO1_B4
D9 = pin.GPIO1_B1
D10 = pin.GPIO1_B2
D11 = pin.GPIO1_B3
D12 = pin.GPIO3_C2
D13 = pin.GPIO3_A7
D14 = pin.GPIO0_B5
D15 = pin.GPIO0_B6
D16 = pin.GPIO3_B1
D17 = pin.GPIO3_C1
D18 = pin.GPIO3_B5
D19 = pin.GPIO3_B6
D20 = pin.GPIO3_B2
D21 = pin.GPIO3_B3
D22 = pin.GPIO3_C0
D23 = pin.GPIO3_A4
D24 = pin.GPIO4_C4
# D25 = SAR ADC 4
# D26 = NC
D27 = pin.GPIO3_B7

SDA = pin.I2C1_SDA
SCL = pin.I2C1_SCL

SCLK = pin.SPI3_SCLK
MOSI = pin.SPI3_MOSI
MISO = pin.SPI3_MISO
SCK = SCLK

UART_TX = pin.UART2_TX
UART_RX = pin.UART2_RX
