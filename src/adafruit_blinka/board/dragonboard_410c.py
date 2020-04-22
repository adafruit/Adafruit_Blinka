"""Pin definitions for the Dragonboard 410c."""

from adafruit_blinka.microcontroller.snapdragon.apq8016 import pin

GPIO_A = pin.GPIO_36
GPIO_B = pin.GPIO_12
GPIO_C = pin.GPIO_13
GPIO_D = pin.GPIO_69
GPIO_E = pin.GPIO_115
GPIO_F = pin.PM_MPP_4
GPIO_G = pin.GPIO_24
GPIO_H = pin.GPIO_25
GPIO_I = pin.GPIO_35
GPIO_J = pin.GPIO_34
GPIO_K = pin.GPIO_28
GPIO_L = pin.GPIO_33

GPIO_36 = pin.GPIO_36
GPIO_12 = pin.GPIO_12
GPIO_13 = pin.GPIO_13
GPIO_69 = pin.GPIO_69
GPIO_115 = pin.GPIO_115
GPIO_4 = pin.PM_MPP_4
GPIO_24 = pin.GPIO_24
GPIO_25 = pin.GPIO_25
GPIO_35 = pin.GPIO_35
GPIO_34 = pin.GPIO_34
GPIO_28 = pin.GPIO_28
GPIO_33 = pin.GPIO_33

SDA = pin.I2C0_SDA
SCL = pin.I2C0_SCL

I2C0_SDA = pin.I2C0_SDA
I2C0_SCL = pin.I2C0_SCL
I2C1_SDA = pin.I2C1_SDA
I2C1_SCL = pin.I2C1_SCL

SCLK = pin.SPI0_SCLK
MOSI = pin.SPI0_MOSI
MISO = pin.SPI0_MISO
SPI_CS = pin.SPI0_CS
