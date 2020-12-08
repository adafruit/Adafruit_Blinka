"""Pin definitions for the Coral Dev Board."""

from adafruit_blinka.microcontroller.nxp_imx8m import pin

# Board name = RPI name [= alias] = pin name
I2C2_SDA = D2 = SDA = pin.I2C2_SDA
I2C2_SCL = D3 = SCL = pin.I2C2_SCL

PWM1 = D12 = pin.PWM1
PWM2 = D13 = pin.PWM2
PWM3 = D22 = pin.PWM3

GPIO_P13 = D27 = pin.GPIO6
GPIO_P16 = D23 = pin.GPIO73
GPIO_P18 = D24 = pin.GPIO138
GPIO_P29 = D5 = pin.GPIO7
GPIO_P31 = D6 = pin.GPIO8
GPIO_P36 = D16 = pin.GPIO141
GPIO_P37 = D26 = pin.GPIO77

ECSPI1_MISO = D9 = MISO = pin.ECSPI1_MISO
ECSPI1_MOSI = D10 = MOSI = pin.ECSPI1_MOSI
ECSPI1_SCLK = D11 = SCLK = SCK = pin.ECSPI1_SCLK
ECSPI1_SS0 = D8 = SS0 = pin.ECSPI1_SS0
