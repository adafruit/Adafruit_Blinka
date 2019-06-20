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

SDA = pin.I2C0_SDA
SCL = pin.I2C0_SCL

SCLK = pin.SPI0_SCLK
MOSI = pin.SPI0_MOSI
MISO = pin.SPI0_MISO
SPI_CS = pin.SPI0_CS

