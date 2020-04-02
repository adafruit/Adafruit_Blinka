from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# Ref:
# Linux kernel 4.9.y (hardkernel)
#     linux/include/dt-bindings/gpio/meson-g12a-gpio.h
#     linux/arch/arm64/boot/dts/amlogic/meson64_odroidc4.dts

GPIOAO_0 = GPIO496 = Pin((0, 0))
GPIOAO_1 = GPIO497 = Pin((0, 1))
GPIOAO_2 = GPIO498 = Pin((0, 2))
GPIOAO_3 = GPIO499 = Pin((0, 3))
GPIOAO_4 = GPIO500 = Pin((0, 4))
GPIOAO_5 = GPIO501 = Pin((0, 5))
GPIOAO_6 = GPIO502 = Pin((0, 6))
GPIOAO_7 = GPIO503 = Pin((0, 7))
GPIOAO_8 = GPIO504 = Pin((0, 8))
GPIOAO_9 = GPIO505 = Pin((0, 9))
GPIOAO_10 = GPIO506 = Pin((0, 10))
GPIOAO_11 = GPIO507 = Pin((0, 11))
GPIOE_0 = GPIO508 = Pin((0, 12))
GPIOE_1 = GPIO509 = Pin((0, 13))
GPIOE_2 = GPIO510 = Pin((0, 14))
GPIO_TEST_N = GPIO511 = Pin((0, 15))

GPIOH_0 = GPIO427 = Pin((1, 17))
GPIOH_1 = GPIO428 = Pin((1, 18))
GPIOH_2 = GPIO429 = Pin((1, 19))
GPIOH_3 = GPIO430 = Pin((1, 20))
GPIOH_4 = GPIO431 = Pin((1, 21))
GPIOH_5 = GPIO432 = Pin((1, 22))
GPIOH_6 = GPIO433 = Pin((1, 23))
GPIOH_7 = GPIO434 = Pin((1, 24))
GPIOH_8 = GPIO435 = Pin((1, 25))

GPIOA_0 = GPIO460 = Pin((1, 50))
GPIOA_1 = GPIO461 = Pin((1, 51))
GPIOA_2 = GPIO462 = Pin((1, 52))
GPIOA_3 = GPIO463 = Pin((1, 53))
GPIOA_4 = GPIO464 = Pin((1, 54))
GPIOA_5 = GPIO465 = Pin((1, 55))
GPIOA_6 = GPIO466 = Pin((1, 56))
GPIOA_7 = GPIO467 = Pin((1, 57))
GPIOA_8 = GPIO468 = Pin((1, 58))
GPIOA_9 = GPIO469 = Pin((1, 59))
GPIOA_10 = GPIO470 = Pin((1, 60))
GPIOA_11 = GPIO471 = Pin((1, 61))
GPIOA_12 = GPIO472 = Pin((1, 62))
GPIOA_13 = GPIO473 = Pin((1, 63))
GPIOA_14 = GPIO474 = Pin((1, 64))
GPIOA_15 = GPIO475 = Pin((1, 65))

GPIOX_0 = GPIO476 = Pin((1, 66))
GPIOX_1 = GPIO477 = Pin((1, 67))
GPIOX_2 = GPIO478 = Pin((1, 68))
GPIOX_3 = GPIO479 = Pin((1, 69))
GPIOX_4 = GPIO480 = Pin((1, 70))
GPIOX_5 = GPIO481 = Pin((1, 71))
GPIOX_6 = GPIO482 = Pin((1, 72))
GPIOX_7 = GPIO483 = Pin((1, 73))
GPIOX_8 = GPIO484 = Pin((1, 74))
GPIOX_9 = GPIO485 = Pin((1, 75))
GPIOX_10 = GPIO486 = Pin((1, 76))
GPIOX_11 = GPIO487 = Pin((1, 77))
GPIOX_12 = GPIO488 = Pin((1, 78))
GPIOX_13 = GPIO489 = Pin((1, 79))
GPIOX_14 = GPIO490 = Pin((1, 80))
GPIOX_15 = GPIO491 = Pin((1, 81))
GPIOX_16 = GPIO492 = Pin((1, 82))
GPIOX_17 = GPIO493 = Pin((1, 83))
GPIOX_18 = GPIO494 = Pin((1, 84))
GPIOX_19 = GPIO495 = Pin((1, 85))

I2C1_SDA = GPIOX_17
I2C1_SCL = GPIOX_18
I2C2_SDA = GPIOA_14
I2C2_SCL = GPIOA_15

UART1_TX = GPIOX_12
UART1_RX = GPIOX_13

SPI0_SCLK = GPIOX_11
SPI0_MISO = GPIOX_9
SPI0_MOSI = GPIOX_8
SPI0_CS0 = GPIOX_10

i2cPorts = ((1, I2C1_SCL, I2C1_SDA), (2, I2C2_SCL, I2C2_SDA), )
# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO), )
# ordered as uartId, txId, rxId
uartPorts = ((1, UART1_TX, UART1_RX), )
