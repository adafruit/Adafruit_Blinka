"""
Samsum Exynos5422
Ref:
    Linux kernel 4.14.y (hardkernel)
"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

GPIOA0_0 = GPIO171 = Pin((26, 0))
GPIOA0_1 = GPIO172 = Pin((26, 1))
GPIOA0_2 = GPIO173 = Pin((26, 2))
GPIOA0_3 = GPIO174 = Pin((26, 3))
GPIOA0_4 = GPIO175 = Pin((26, 4))
GPIOA0_5 = GPIO176 = Pin((26, 5))
GPIOA0_6 = GPIO177 = Pin((26, 6))
GPIOA0_6 = GPIO178 = Pin((26, 7))

GPIOA2_0 = GPIO185 = Pin((28, 0))
GPIOA2_1 = GPIO186 = Pin((28, 1))
GPIOA2_2 = GPIO187 = Pin((28, 2))
GPIOA2_3 = GPIO188 = Pin((28, 3))
GPIOA2_4 = GPIO189 = Pin((28, 4))
GPIOA2_5 = GPIO190 = Pin((28, 5))
GPIOA2_6 = GPIO191 = Pin((28, 6))
GPIOA2_7 = GPIO192 = Pin((28, 7))

GPIOB3_0 = GPIO207 = Pin((32, 0))
GPIOB3_1 = GPIO208 = Pin((32, 1))
GPIOB3_2 = GPIO209 = Pin((32, 2))
GPIOB3_3 = GPIO210 = Pin((32, 3))
GPIOB3_4 = GPIO211 = Pin((32, 4))
GPIOB3_5 = GPIO212 = Pin((32, 5))
GPIOB3_6 = GPIO213 = Pin((32, 6))
GPIOB3_7 = GPIO214 = Pin((32, 7))

GPIOX1_0 = GPIO16 = Pin((2, 0))
GPIOX1_1 = GPIO17 = Pin((2, 1))
GPIOX1_2 = GPIO18 = Pin((2, 2))
GPIOX1_3 = GPIO19 = Pin((2, 3))
GPIOX1_4 = GPIO20 = Pin((2, 4))
GPIOX1_5 = GPIO21 = Pin((2, 5))
GPIOX1_6 = GPIO22 = Pin((2, 6))
GPIOX1_7 = GPIO23 = Pin((2, 7))

GPIOX2_0 = GPIO24 = Pin((3, 0))
GPIOX2_1 = GPIO25 = Pin((3, 1))
GPIOX2_2 = GPIO26 = Pin((3, 2))
GPIOX2_3 = GPIO27 = Pin((3, 3))
GPIOX2_4 = GPIO28 = Pin((3, 4))
GPIOX2_5 = GPIO29 = Pin((3, 5))
GPIOX2_6 = GPIO30 = Pin((3, 6))
GPIOX2_7 = GPIO31 = Pin((3, 7))

GPIOX3_0 = GPIO32 = Pin((4, 0))
GPIOX3_1 = GPIO33 = Pin((4, 1))
GPIOX3_2 = GPIO34 = Pin((4, 2))
GPIOX3_3 = GPIO35 = Pin((4, 3))
GPIOX3_4 = GPIO36 = Pin((4, 4))
GPIOX3_5 = GPIO37 = Pin((4, 5))
GPIOX3_6 = GPIO38 = Pin((4, 6))
GPIOX3_7 = GPIO39 = Pin((4, 7))

I2C1_SDA = GPIOB3_2
I2C1_SCL = GPIOB3_3
I2C5_SDA = GPIOA2_2
I2C5_SCL = GPIOA2_3

UART0_TX = GPIOA0_1
UART0_RX = GPIOA0_0

SPI1_SCLK = GPIOA2_4
SPI1_MISO = GPIOA2_6
SPI1_MOSI = GPIOA2_7
SPI1_CS0 = GPIOA2_5

# ordered as i2cId, sclId, sdaId
i2cPorts = (
    (1, I2C1_SCL, I2C1_SDA),
    (5, I2C5_SCL, I2C5_SDA),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),)

# ordered as uartId, txId, rxId
uartPorts = ((0, UART0_TX, UART0_RX),)
