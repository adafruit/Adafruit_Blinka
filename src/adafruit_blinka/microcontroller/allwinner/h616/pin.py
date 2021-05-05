"""Allwinner H616 Pin Names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PC0 = Pin((1, 64))
SPI0_SCLK = PC0
PC1 = Pin((1, 65))
PC2 = Pin((1, 66))
SPI0_MOSI = PC2
PC3 = Pin((1, 67))
SPI0_CS0 = PC3
PC4 = Pin((1, 68))
SPI0_MISO = PC4
PC5 = Pin((1, 69))
PC6 = Pin((1, 70))
PC7 = Pin((1, 71))
PC8 = Pin((1, 72))
PC9 = Pin((1, 73))
PC10 = Pin((1, 74))
PC11 = Pin((1, 75))
PC12 = Pin((1, 76))
PC13 = Pin((1, 77))
PC14 = Pin((1, 78))
PC15 = Pin((1, 79))

PF0 = Pin((1, 160))
PF1 = Pin((1, 161))
PF2 = Pin((1, 162))
PF3 = Pin((1, 163))
PF4 = Pin((1, 164))
PF5 = Pin((1, 165))
PF6 = Pin((1, 166))

PG0 = Pin((1, 192))
PG1 = Pin((1, 193))
PG2 = Pin((1, 194))
PG3 = Pin((1, 195))
PG4 = Pin((1, 196))
PG5 = Pin((1, 197))
PG6 = Pin((1, 198))
PG7 = Pin((1, 199))
PG8 = Pin((1, 200))
PG9 = Pin((1, 201))
PG10 = Pin((1, 202))
PG11 = Pin((1, 203))
PG12 = Pin((1, 204))
PG13 = Pin((1, 205))
PG14 = Pin((1, 206))
PG15 = Pin((1, 207))
PG16 = Pin((1, 208))
PG17 = Pin((1, 209))
PG18 = Pin((1, 210))
PG19 = Pin((1, 211))

PH0 = Pin((1, 224))
PH1 = Pin((1, 225))
PH2 = Pin((1, 226))
UART5_TX = PH2
PH3 = Pin((1, 227))
UART5_RX = PH3
PH4 = Pin((1, 228))
TWI3_SCL = PH4
PH5 = Pin((1, 229))
UART2_TX = PH5
TWI3_SDA = PH5
SPI1_CS0 = PH5
PH6 = Pin((1, 230))
UART2_RX = PH6
SPI1_SCLK = PH6
PH7 = Pin((1, 231))
SPI1_MOSI = PH7
PH8 = Pin((1, 232))
SPI1_MISO = PH8
PH9 = Pin((1, 233))
SPI1_CS1 = PH9
PH10 = Pin((1, 234))

PI0 = Pin((1, 256))
PI1 = Pin((1, 257))
PI2 = Pin((1, 258))
PI3 = Pin((1, 259))
PI4 = Pin((1, 260))
PI5 = Pin((1, 261))
PI6 = Pin((1, 262))
PI7 = Pin((1, 263))
PI8 = Pin((1, 264))
PI9 = Pin((1, 265))
PI10 = Pin((1, 266))
PI11 = Pin((1, 267))
PI12 = Pin((1, 268))
PI13 = Pin((1, 269))
PI14 = Pin((1, 270))
PI15 = Pin((1, 271))
PI16 = Pin((1, 272))

i2cPorts = ((3, TWI3_SCL, TWI3_SDA),)
# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),
    (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),
)
# ordered as uartId, txId, rxId
uartPorts = (
    (2, UART2_TX, UART2_RX),
    (5, UART5_TX, UART5_RX),
)
