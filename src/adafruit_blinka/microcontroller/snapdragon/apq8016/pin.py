"""SnapDragon APQ8016 pin names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

GPIO_0 = Pin((0, 0))
GPIO_1 = Pin((0, 1))
GPIO_2 = Pin((0, 2))
GPIO_3 = Pin((0, 3))
GPIO_4 = Pin((0, 4))
GPIO_5 = Pin((0, 5))
GPIO_6 = Pin((0, 6))
GPIO_7 = Pin((0, 7))
GPIO_8 = Pin((0, 8))
GPIO_9 = Pin((0, 9))
GPIO_10 = Pin((0, 10))
GPIO_11 = Pin((0, 11))
GPIO_12 = Pin((0, 12))
GPIO_13 = Pin((0, 13))
GPIO_14 = Pin((0, 14))
GPIO_15 = Pin((0, 15))
GPIO_16 = Pin((0, 16))
GPIO_17 = Pin((0, 17))
GPIO_18 = Pin((0, 18))
GPIO_19 = Pin((0, 19))
GPIO_20 = Pin((0, 20))

GPIO_22 = Pin((0, 22))
GPIO_23 = Pin((0, 23))
GPIO_24 = Pin((0, 24))
GPIO_25 = Pin((0, 25))
GPIO_26 = Pin((0, 26))
GPIO_27 = Pin((0, 27))
GPIO_28 = Pin((0, 28))
GPIO_29 = Pin((0, 29))
GPIO_30 = Pin((0, 30))

GPIO_33 = Pin((0, 33))
GPIO_34 = Pin((0, 34))
GPIO_35 = Pin((0, 35))
GPIO_36 = Pin((0, 36))
GPIO_37 = Pin((0, 37))

GPIO_39 = Pin((0, 39))
GPIO_40 = Pin((0, 40))
GPIO_41 = Pin((0, 41))
GPIO_42 = Pin((0, 42))
GPIO_43 = Pin((0, 43))
GPIO_44 = Pin((0, 44))
GPIO_45 = Pin((0, 45))
GPIO_46 = Pin((0, 46))
GPIO_47 = Pin((0, 47))
GPIO_48 = Pin((0, 48))
GPIO_49 = Pin((0, 49))
GPIO_50 = Pin((0, 50))
GPIO_51 = Pin((0, 51))
GPIO_52 = Pin((0, 52))
GPIO_53 = Pin((0, 53))
GPIO_54 = Pin((0, 54))
GPIO_55 = Pin((0, 55))
GPIO_56 = Pin((0, 56))
GPIO_57 = Pin((0, 57))
GPIO_58 = Pin((0, 58))
GPIO_59 = Pin((0, 59))
GPIO_60 = Pin((0, 60))
GPIO_61 = Pin((0, 61))
GPIO_62 = Pin((0, 62))
GPIO_63 = Pin((0, 63))
GPIO_64 = Pin((0, 64))
GPIO_65 = Pin((0, 65))
GPIO_66 = Pin((0, 66))
GPIO_67 = Pin((0, 67))
GPIO_68 = Pin((0, 68))
GPIO_69 = Pin((0, 69))
GPIO_70 = Pin((0, 70))
GPIO_71 = Pin((0, 71))
GPIO_72 = Pin((0, 72))
GPIO_73 = Pin((0, 73))
GPIO_74 = Pin((0, 74))
GPIO_75 = Pin((0, 75))
GPIO_76 = Pin((0, 76))
GPIO_77 = Pin((0, 77))
GPIO_78 = Pin((0, 78))
GPIO_79 = Pin((0, 79))
GPIO_80 = Pin((0, 80))
GPIO_81 = Pin((0, 81))
GPIO_82 = Pin((0, 82))
GPIO_83 = Pin((0, 83))
GPIO_84 = Pin((0, 84))
GPIO_85 = Pin((0, 85))
GPIO_86 = Pin((0, 86))
GPIO_87 = Pin((0, 87))
GPIO_88 = Pin((0, 88))
GPIO_89 = Pin((0, 89))
GPIO_90 = Pin((0, 90))
GPIO_91 = Pin((0, 91))
GPIO_92 = Pin((0, 92))
GPIO_93 = Pin((0, 93))
GPIO_94 = Pin((0, 94))
GPIO_95 = Pin((0, 95))
GPIO_96 = Pin((0, 96))
GPIO_97 = Pin((0, 97))
GPIO_98 = Pin((0, 98))
GPIO_99 = Pin((0, 99))
GPIO_100 = Pin((0, 100))
GPIO_101 = Pin((0, 101))
GPIO_102 = Pin((0, 102))
GPIO_103 = Pin((0, 103))
GPIO_104 = Pin((0, 104))
GPIO_105 = Pin((0, 105))
GPIO_106 = Pin((0, 106))

GPIO_108 = Pin((0, 108))
GPIO_109 = Pin((0, 109))
GPIO_110 = Pin((0, 110))
GPIO_111 = Pin((0, 111))
GPIO_112 = Pin((0, 112))
GPIO_113 = Pin((0, 113))
GPIO_114 = Pin((0, 114))
GPIO_115 = Pin((0, 115))
GPIO_116 = Pin((0, 116))
GPIO_117 = Pin((0, 117))
GPIO_118 = Pin((0, 118))
GPIO_119 = Pin((0, 119))

PM_GPIO_0 = Pin((1, 0))
PM_GPIO_1 = Pin((1, 1))
PM_GPIO_2 = Pin((1, 2))
PM_GPIO_3 = Pin((1, 3))

PM_MPP_1 = Pin((2, 0))
PM_MPP_2 = Pin((2, 1))
PM_MPP_3 = Pin((2, 2))
PM_MPP_4 = Pin((2, 3))

I2C0_SDA = GPIO_6
I2C0_SCL = GPIO_7
I2C1_SDA = GPIO_22
I2C1_SCL = GPIO_23

UART0_TX = GPIO_0
UART0_RX = GPIO_1
UART1_TX = GPIO_4
UART1_RX = GPIO_5

SPI0_SCLK = GPIO_19
SPI0_MISO = GPIO_17
SPI0_MOSI = GPIO_16
SPI0_CS = GPIO_18

i2cPorts = (
    (0, I2C0_SCL, I2C0_SDA),
    (1, I2C1_SCL, I2C1_SDA),
)
# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),)
# ordered as uartId, txId, rxId
uartPorts = (
    (0, UART0_TX, UART0_RX),
    (1, UART1_TX, UART1_RX),
)
