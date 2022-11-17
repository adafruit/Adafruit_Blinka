"""A Pin class for use with Rockchip RK3568B2."""

from adafruit_blinka.microcontroller.generic_linux.sysfs_pin import Pin

GPIO3C_6 = pin((3, 22))
GPIO3C_7 = pin((3, 23))
GPIO3D_0 = pin((3, 24))
GPIO3D_1 = pin((3, 25))
GPIO3D_2 = pin((3, 26))
GPIO3D_3 = pin((3, 27))
GPIO3D_4 = pin((3, 28))
GPIO3D_5 = pin((3, 29))
GPIO3D_6 = pin((3, 30))
GPIO3D_7 = pin((3, 31))
GPIO3B_2 = pin((3, 10))
GPIO3B_5 = pin((3, 13))
GPIO3B_6 = pin((3, 14))
GPIO0B_3 = pin((0, 11))
GPIO0B_4 = pin((0, 12))
GPIO0B_5 = pin((0, 13))
GPIO0B_6 = pin((0, 14))
GPIO0C_0 = pin((0, 16))
GPIO0C_1 = pin((0, 17))
GPIO2D_0 = pin((2, 24))
GPIO2D_1 = pin((2, 25))
GPIO2D_2 = pin((2, 26))
GPIO2D_3 = pin((2, 27))
GPIO4B_6 = pin((4, 14))
GPIO4C_1 = pin((4, 17))
ADC_AIN0 = 37
ADC_AIN1 = 40

# I2C
I2C0_SCL = GPIO3B_5
I2C0_SDA = GPIO3B_6
I2C1_SCL = GPIO0B_3
I2C1_SDA = GPIO0B_4

# SPI
SPI0_CS = GPIO2D_2
SPI0_SCLK = GPIO2D_3
SPI0_MISO = GPIO2D_0
SPI0_MOSI = GPIO2D_1


# UART
UART0_TX = GPIO0C_1
UART0_RX = GPIO0C_0
UART1_TX = GPIO3D_6
UART1_RX = GPIO3D_7

# PWM
#PWM0 = GPIO4_C2
#PWM1 = GPIO4_C6

# ordered as i2cId, SCL, SDA
i2cPorts = (
    (0, I2C0_SCL, I2C0_SDA),
    (1, I2C1_SCL, I2C1_SDA),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((1, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),)

# SysFS pwm outputs, pwm channel and pin in first tuple
#pwmOuts = (
#    ((0, 0), PWM0),
#   ((1, 0), PWM1),
#)

# SysFS analog inputs, Ordered as analog analogInId, device, and channel
analogIns = (
            (ADC_AIN0, 0, 0),
            (ADC_AIN1, 0, 0),
            )
