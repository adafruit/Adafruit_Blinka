"""Pin definitions for the Odroid XU4."""

from adafruit_blinka.microcontroller.samsung.exynos5422 import pin

SDA = SDA1 = pin.I2C1_SDA
SCL = SCL1 = pin.I2C1_SCL
SDA5 = pin.I2C5_SDA
SCL5 = pin.I2C5_SCL

SCLK = pin.SPI1_SCLK
MOSI = pin.SPI1_MOSI
MISO = pin.SPI1_MISO
SPI_CS0 = pin.SPI1_CS0

"""physical pin number(XU4 Shifter Shield)"""

D3 = pin.GPIOB3_2
D5 = pin.GPIOB3_3
D7 = pin.GPIOX1_2
D8 = pin.GPIOA0_1
D10 = pin.GPIOA0_0
D11 = pin.GPIOA0_3
D12 = pin.GPIOA0_2
D13 = pin.GPIOX1_5
D15 = pin.GPIOX1_6
D16 = pin.GPIOX1_3
D18 = pin.GPIOX1_7
D19 = pin.GPIOA2_7
D21 = pin.GPIOA2_6
D22 = pin.GPIOX2_0
D23 = pin.GPIOA2_4
D24 = pin.GPIOA2_5
D26 = pin.GPIOX2_1
D27 = pin.GPIOA2_2
D28 = pin.GPIOA2_4
D29 = pin.GPIOX2_4
D31 = pin.GPIOX2_6
D32 = pin.GPIOX2_5
D33 = pin.GPIOX2_7
D36 = pin.GPIOX3_1
