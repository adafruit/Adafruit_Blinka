"""A Pin class for use with Rockchip RK3308."""

from adafruit_blinka.microcontroller.generic_linux.sysfs_pin import Pin

GPIO0_A0 = Pin(0)
GPIO0_A1 = Pin(1)
GPIO0_A2 = Pin(2)
GPIO0_A3 = Pin(3)
GPIO0_A4 = Pin(4)
GPIO0_A5 = Pin(5)
GPIO0_A6 = Pin(6)
GPIO0_A7 = Pin(7)
GPIO0_B0 = Pin(8)
GPIO0_B1 = Pin(9)
GPIO0_B2 = Pin(10)
GPIO0_B3 = Pin(11)
GPIO0_B4 = Pin(12)
GPIO0_B5 = Pin(13)
GPIO0_B6 = Pin(14)
GPIO0_B7 = Pin(15)
GPIO0_C0 = Pin(16)
GPIO0_C1 = Pin(17)
GPIO0_C2 = Pin(18)
GPIO0_C3 = Pin(19)
GPIO0_C4 = Pin(20)
GPIO0_C5 = Pin(21)
GPIO0_C6 = Pin(22)
GPIO0_C7 = Pin(23)
GPIO0_D0 = Pin(24)
GPIO0_D1 = Pin(25)
GPIO0_D2 = Pin(26)
GPIO0_D3 = Pin(27)
GPIO0_D4 = Pin(28)
GPIO0_D5 = Pin(29)
GPIO0_D6 = Pin(30)
GPIO0_D7 = Pin(31)
GPIO1_A0 = Pin(32)
GPIO1_A1 = Pin(33)
GPIO1_A2 = Pin(34)
GPIO1_A3 = Pin(35)
GPIO1_A4 = Pin(36)
GPIO1_A5 = Pin(37)
GPIO1_A6 = Pin(38)
GPIO1_A7 = Pin(39)
GPIO1_B0 = Pin(40)
GPIO1_B1 = Pin(41)
GPIO1_B2 = Pin(42)
GPIO1_B3 = Pin(43)
GPIO1_B4 = Pin(44)
GPIO1_B5 = Pin(45)
GPIO1_B6 = Pin(46)
GPIO1_B7 = Pin(47)
GPIO1_C0 = Pin(48)
GPIO1_C1 = Pin(49)
GPIO1_C2 = Pin(50)
GPIO1_C3 = Pin(51)
GPIO1_C4 = Pin(52)
GPIO1_C5 = Pin(53)
GPIO1_C6 = Pin(54)
GPIO1_C7 = Pin(55)
GPIO1_D0 = Pin(56)
GPIO1_D1 = Pin(57)
GPIO1_D2 = Pin(58)
GPIO1_D3 = Pin(59)
GPIO1_D4 = Pin(60)
GPIO1_D5 = Pin(61)
GPIO1_D6 = Pin(62)
GPIO1_D7 = Pin(63)
GPIO2_A0 = Pin(64)
GPIO2_A1 = Pin(65)
GPIO2_A2 = Pin(66)
GPIO2_A3 = Pin(67)
GPIO2_A4 = Pin(68)
GPIO2_A5 = Pin(69)
GPIO2_A6 = Pin(70)
GPIO2_A7 = Pin(71)
GPIO2_B0 = Pin(72)
GPIO2_B1 = Pin(73)
GPIO2_B2 = Pin(74)
GPIO2_B3 = Pin(75)
GPIO2_B4 = Pin(76)
GPIO2_B5 = Pin(77)
GPIO2_B6 = Pin(78)
GPIO2_B7 = Pin(79)
GPIO2_C0 = Pin(80)
GPIO2_C1 = Pin(81)
GPIO2_C2 = Pin(82)
GPIO2_C3 = Pin(83)
GPIO2_C4 = Pin(84)
GPIO2_C5 = Pin(85)
GPIO2_C6 = Pin(86)
GPIO2_C7 = Pin(87)
GPIO2_D0 = Pin(88)
GPIO2_D1 = Pin(89)
GPIO2_D2 = Pin(90)
GPIO2_D3 = Pin(91)
GPIO2_D4 = Pin(92)
GPIO2_D5 = Pin(93)
GPIO2_D6 = Pin(94)
GPIO2_D7 = Pin(95)
GPIO3_A0 = Pin(96)
GPIO3_A1 = Pin(97)
GPIO3_A2 = Pin(98)
GPIO3_A3 = Pin(99)
GPIO3_A4 = Pin(100)
GPIO3_A5 = Pin(101)
GPIO3_A6 = Pin(102)
GPIO3_A7 = Pin(103)
GPIO3_B0 = Pin(104)
GPIO3_B1 = Pin(105)
GPIO3_B2 = Pin(106)
GPIO3_B3 = Pin(107)
GPIO3_B4 = Pin(108)
GPIO3_B5 = Pin(109)
GPIO3_B6 = Pin(110)
GPIO3_B7 = Pin(111)
GPIO3_C0 = Pin(112)
GPIO3_C1 = Pin(113)
GPIO3_C2 = Pin(114)
GPIO3_C3 = Pin(115)
GPIO3_C4 = Pin(116)
GPIO3_C5 = Pin(117)
GPIO3_C6 = Pin(118)
GPIO3_C7 = Pin(119)
GPIO3_D0 = Pin(120)
GPIO3_D1 = Pin(121)
GPIO3_D2 = Pin(122)
GPIO3_D3 = Pin(123)
GPIO3_D4 = Pin(124)
GPIO3_D5 = Pin(125)
GPIO3_D6 = Pin(126)
GPIO3_D7 = Pin(127)
ADC_IN0 = 1


# I2C
I2C0_SDA = GPIO1_D0
I2C0_SCL = GPIO1_D1
I2C1_SDA = GPIO0_B3
I2C1_SCL = GPIO0_B4
I2C2_SDA = GPIO2_A2
I2C2_SCL = GPIO2_A3
I2C3_SDA = GPIO0_B7
I2C3_SCL = GPIO0_C0

# SPI
SPI2_CS = GPIO1_D1
SPI2_SCLK = GPIO1_D0
SPI2_MISO = GPIO1_C6
SPI2_MOSI = GPIO1_C7

# UART
UART0_TX = GPIO2_A1
UART0_RX = GPIO2_A0
UART1_TX = GPIO1_D1
UART1_RX = GPIO1_D0
UART2_TX = GPIO1_C7
UART2_RX = GPIO1_C6

# PWM
PWM2 = GPIO0_B7
PWM3 = GPIO0_C0

# ordered as i2cId, SCL, SDA
i2cPorts = (
    (0, I2C0_SCL, I2C0_SDA),
    (1, I2C1_SCL, I2C1_SDA),
    (2, I2C2_SCL, I2C2_SDA),
    (3, I2C3_SCL, I2C3_SDA),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((2, SPI2_SCLK, SPI2_MOSI, SPI2_MISO),)

# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = (
    ((1, 0), PWM2),
    ((2, 0), PWM3),
)

# SysFS analog inputs, Ordered as analog analogInId, device, and channel
analogIns = ((ADC_IN0, 0, 0),)
