from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

GPIO496 = Pin((0, 0))
GPIO497 = Pin((0, 1))
GPIO498 = Pin((0, 2))
GPIO499 = Pin((0, 3))
GPIO500 = Pin((0, 4))
GPIO501 = Pin((0, 5))
GPIO502 = Pin((0, 6))
GPIO503 = Pin((0, 7))
GPIO504 = Pin((0, 8))
GPIO505 = Pin((0, 9))
GPIO506 = Pin((0, 10))
GPIO507 = Pin((0, 11))
GPIO508 = Pin((0, 12))
GPIO509 = Pin((0, 13))
GPIO510 = Pin((0, 14))
GPIO511 = Pin((0, 15))

GPIO17 = Pin((1, 17))
GPIO18 = Pin((1, 18))
GPIO19 = Pin((1, 19))
GPIO20 = Pin((1, 20))
GPIO21 = Pin((1, 21))
GPIO22 = Pin((1, 22))
GPIO23 = Pin((1, 23))
GPIO24 = Pin((1, 24))
GPIO25 = Pin((1, 25))

GPIO460 = Pin((1, 50))
GPIO461 = Pin((1, 51))
GPIO462 = Pin((1, 52))
GPIO463 = Pin((1, 53))
GPIO464 = Pin((1, 54))
GPIO465 = Pin((1, 55))
GPIO466 = Pin((1, 56))
GPIO467 = Pin((1, 57))
GPIO468 = Pin((1, 58))
GPIO469 = Pin((1, 59))
GPIO470 = Pin((1, 60))
GPIO472 = Pin((1, 62))
GPIO471 = Pin((1, 61))
GPIO472 = Pin((1, 62))
GPIO473 = Pin((1, 63))
GPIO474 = Pin((1, 64))
GPIO475 = Pin((1, 65))
GPIO476 = Pin((1, 66))
GPIO477 = Pin((1, 67))
GPIO478 = Pin((1, 68))
GPIO479 = Pin((1, 69))
GPIO480 = Pin((1, 70))
GPIO481 = Pin((1, 71))
GPIO482 = Pin((1, 72))
GPIO483 = Pin((1, 73))
GPIO484 = Pin((1, 74))
GPIO485 = Pin((1, 75))
GPIO486 = Pin((1, 76))
GPIO487 = Pin((1, 77))
GPIO488 = Pin((1, 78))
GPIO489 = Pin((1, 79))
GPIO490 = Pin((1, 80))
GPIO491 = Pin((1, 81))
GPIO492 = Pin((1, 82))
GPIO493 = Pin((1, 83))
GPIO494 = Pin((1, 84))
GPIO495 = Pin((1, 85))

I2C2_SDA = GPIO493
I2C2_SCL = GPIO494
I2C3_SDA = GPIO474
I2C3_SCL = GPIO475

UART1_TX = GPIO488
UART1_RX = GPIO489

SPI0_SCLK = GPIO487
SPI0_MISO = GPIO485
SPI0_MOSI = GPIO484
SPI0_CS0 = GPIO488

i2cPorts = ( (2, I2C2_SCL, I2C2_SDA), (3, I2C3_SCL, I2C3_SDA), )
# ordered as spiId, sckId, mosiId, misoId
spiPorts = ( (0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO), )
# ordered as uartId, txId, rxId
uartPorts = ( (1, UART1_TX, UART1_RX), )
