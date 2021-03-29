"""Pin definitions for the Coral Dev Board Mini."""

from adafruit_blinka.microcontroller.mt8167 import pin

# Board name = RPI name [= alias] = pin name
GPIO22 = D4 = pin.GPIO22  # Pin 7
GPIO9 = D17 = pin.GPIO9  # Pin 11
GPIO36 = D18 = pin.GPIO36  # Pin 12
GPIO10 = D27 = pin.GPIO10  # Pin 13
GPIO0 = D23 = pin.GPIO0  # Pin 16
GPIO1 = D24 = pin.GPIO1  # Pin 18
GPIO7 = D25 = pin.GPIO7  # Pin 22
GPIO8 = D7 = pin.GPIO8  # Pin 26
GPIO37 = D19 = pin.GPIO37  # Pin 35
GPIO13 = D16 = pin.GPIO13  # Pin 36
GPIO45 = D26 = pin.GPIO45  # Pin 37
GPIO38 = D20 = pin.GPIO38  # Pin 38
GPIO39 = D21 = pin.GPIO39  # Pin 40

I2C1_SDA = D2 = SDA1 = pin.I2C1_SDA  # Pin 3
I2C1_SCL = D3 = SCL1 = pin.I2C1_SCL  # Pin 5
I2C2_SDA = D0 = SDA2 = pin.I2C2_SDA  # Pin 27
I2C2_SCL = D1 = SCL2 = pin.I2C2_SCL  # Pin 28

PWM_A = D12 = pin.PWM_A  # Pin 32
PWM_B = D13 = pin.PWM_B  # Pin 33
PWM_C = D22 = pin.PWM_C  # Pin 15

SPI_MO = D10 = MOSI = pin.SPI_MO  # Pin 19
SPI_MI = D9 = MISO = pin.SPI_MI  # Pin 21
SPI_CLK = D11 = SCLK = pin.SPI_CLK  # Pin 23
SPI_CSB = D8 = CS0 = pin.SPI_CSB  # Pin 24

# UART currently not supported
GPIO63 = D14 = pin.GPIO63  # UART0_TX, Pin 8
GPIO62 = D15 = pin.GPIO62  # UART0_RX, Pin 10
GPIO65 = D5 = pin.GPIO65  # UART1_TX, Pin 29
GPIO64 = D6 = pin.GPIO64  # UART1_RX, Pin 31
