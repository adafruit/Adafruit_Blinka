"""Pin definitions for the Coral Edge TPU Dev board."""

from adafruit_blinka.microcontroller.nxp_imx8m import pin

SDA = pin.I2C2_SDA
SCL = pin.I2C2_SCL


GPIO_P13 = pin.GPIO6
GPIO_P16 = pin.GPIO73
GPIO_P18 = pin.GPIO138
GPIO_P29 = pin.GPIO7
GPIO_P31 = pin.GPIO8
GPIO_P36 = pin.GPIO141
GPIO_P37 = pin.GPIO77

MISO = pin.ECSPI1_MISO
MOSI = pin.ECSPI1_MOSI
SCLK = pin.ECSPI1_SCLK
SCK = pin.ECSPI1_SCLK
SS0 = pin.ECSPI1_SS0

