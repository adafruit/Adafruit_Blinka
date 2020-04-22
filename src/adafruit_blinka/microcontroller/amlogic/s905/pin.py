"""AmLogic s905 pin names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

GPIO122 = Pin((0, 0))
GPIO123 = Pin((0, 1))
GPIO124 = Pin((0, 2))
GPIO125 = Pin((0, 3))
GPIO126 = Pin((0, 4))
GPIO127 = Pin((0, 5))
GPIO128 = Pin((0, 6))
GPIO129 = Pin((0, 7))
GPIO130 = Pin((0, 8))
GPIO131 = Pin((0, 9))
GPIO132 = Pin((0, 10))
GPIO133 = Pin((0, 11))
GPIO134 = Pin((0, 12))
GPIO135 = Pin((0, 13))

GPIO205 = Pin((1, 69))
GPIO206 = Pin((1, 70))
GPIO207 = Pin((1, 71))
GPIO208 = Pin((1, 72))
GPIO209 = Pin((1, 73))
GPIO210 = Pin((1, 74))

GPIO211 = Pin((1, 75))
GPIO212 = Pin((1, 76))
GPIO213 = Pin((1, 77))
GPIO214 = Pin((1, 78))
GPIO215 = Pin((1, 79))
GPIO216 = Pin((1, 80))
GPIO217 = Pin((1, 81))
GPIO218 = Pin((1, 82))
GPIO219 = Pin((1, 83))
GPIO220 = Pin((1, 84))
GPIO221 = Pin((1, 85))
GPIO222 = Pin((1, 86))
GPIO223 = Pin((1, 87))
GPIO224 = Pin((1, 88))
GPIO225 = Pin((1, 89))
GPIO226 = Pin((1, 90))
GPIO227 = Pin((1, 91))

GPIO228 = Pin((1, 92))
GPIO229 = Pin((1, 93))
GPIO230 = Pin((1, 94))
GPIO231 = Pin((1, 95))
GPIO232 = Pin((1, 96))
GPIO233 = Pin((1, 97))
GPIO234 = Pin((1, 98))
GPIO235 = Pin((1, 99))
GPIO236 = Pin((1, 100))
GPIO237 = Pin((1, 101))
GPIO238 = Pin((1, 102))
GPIO239 = Pin((1, 103))
GPIO240 = Pin((1, 104))
GPIO241 = Pin((1, 105))
GPIO242 = Pin((1, 106))
GPIO243 = Pin((1, 107))
GPIO247 = Pin((1, 111))
GPIO248 = Pin((1, 112))
GPIO249 = Pin((1, 113))

I2C0_SDA = GPIO205
I2C0_SCL = GPIO206
I2C1_SDA = GPIO207
I2C1_SCL = GPIO208
I2C2_SDA = GPIO209
I2C2_SCL = GPIO210

UART1_TX = GPIO240
UART1_RX = GPIO241
UART2_TX = GPIO205
UART2_RX = GPIO206

SPI0_SCLK = GPIO230
SPI0_MISO = GPIO232
SPI0_MOSI = GPIO235

i2cPorts = (
    (0, I2C0_SCL, I2C0_SDA),
    (1, I2C1_SCL, I2C1_SDA),
)
# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),)
# ordered as uartId, txId, rxId
uartPorts = (
    (1, UART1_TX, UART1_RX),
    (2, UART2_TX, UART2_RX),
)
