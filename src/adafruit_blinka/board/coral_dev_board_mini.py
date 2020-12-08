"""Pin definitions for the Coral Dev Board Mini."""

from adafruit_blinka.microcontroller.mt8167 import pin

GPIO_P7 = pin.GPIO22
GPIO_P11 = pin.GPIO9
GPIO_P12 = pin.GPIO36
GPIO_P13 = pin.GPIO10
GPIO_P16 = pin.GPIO0
GPIO_P18 = pin.GPIO1
GPIO_P22 = pin.GPIO7
GPIO_P26 = pin.GPIO8
GPIO_P35 = pin.GPIO37
GPIO_P36 = pin.GPIO13
GPIO_P37 = pin.GPIO45
GPIO_P38 = pin.GPIO38
GPIO_P40 = pin.GPIO39

SDA1 = pin.I2C1_SDA
SCL1 = pin.I2C1_SCL

SDA2 = pin.I2C2_SDA
SCL2 = pin.I2C2_SCL

PWM0 = pin.PWM0
PWM1 = pin.PWM1
PWM2 = pin.PWM2

MOSI = pin.SPI_MO
MISO = pin.SPI_MI
SCLK = pin.SPI_CLK
SCK = SCLK
CS0 = pin.SPI_CSB
CS = CS0
