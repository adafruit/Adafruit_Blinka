# SPDX-FileCopyrightText: 2022 MrPanc0 for Adafruit Industries
# SPDX-FileCopyrightText: 2023 Steve Jeong for Hardkernel
#
# SPDX-License-Identifier: MIT

"""A Pin class for use with Rockchip RK3568B2."""

from adafruit_blinka.agnostic import detector
from adafruit_blinka.microcontroller.alias import get_dts_alias, get_pwm_chipid
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

GPIO3C_6 = Pin((3, 22))
GPIO3C_7 = Pin((3, 23))
GPIO3D_0 = Pin((3, 24))
GPIO3D_1 = Pin((3, 25))
GPIO3D_2 = Pin((3, 26))
GPIO3D_3 = Pin((3, 27))
GPIO3D_4 = Pin((3, 28))
GPIO3D_5 = Pin((3, 29))
GPIO3D_6 = Pin((3, 30))
GPIO3D_7 = Pin((3, 31))
GPIO3B_2 = Pin((3, 10))
GPIO3B_5 = Pin((3, 13))
GPIO3B_6 = Pin((3, 14))
GPIO0B_3 = Pin((0, 11))
GPIO0B_4 = Pin((0, 12))
GPIO0B_5 = Pin((0, 13))
GPIO0B_6 = Pin((0, 14))
GPIO0C_0 = Pin((0, 16))
GPIO0C_1 = Pin((0, 17))
GPIO2D_0 = Pin((2, 24))
GPIO2D_1 = Pin((2, 25))
GPIO2D_2 = Pin((2, 26))
GPIO2D_3 = Pin((2, 27))
GPIO4B_6 = Pin((4, 14))
GPIO4C_1 = Pin((4, 17))
ADC_AIN0 = 37
ADC_AIN1 = 40

# I2C
I2C1_SCL = GPIO0B_3
I2C1_SDA = GPIO0B_4

# SPI
SPI0_CS_M1 = GPIO2D_2
SPI0_SCLK_M1 = GPIO2D_3
SPI0_MISO_M1 = GPIO2D_0
SPI0_MOSI_M1 = GPIO2D_1

# UART
UART0_TX = GPIO0C_1
UART0_RX = GPIO0C_0
UART1_TX = GPIO3D_6
UART1_RX = GPIO3D_7

# PWM
# PWM0 = GPIO4_C2
# PWM1 = GPIO4_C6

# ordered as i2cId, SCL, SDA
i2cPorts = [
    (1, I2C1_SCL, I2C1_SDA),
]

# SysFS pwm outputs, pwm channel and pin in first tuple
# pwmOuts = (
#    ((0, 0), PWM0),
#   ((1, 0), PWM1),
# )

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI0_SCLK_M1, SPI0_MOSI_M1, SPI0_MISO_M1),)

# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = []

# ordered as uartId, txId, rxId
uartPorts = []

# SysFS analog inputs, Ordered as analog analogInId, device, and channel
analogIns = []

board = detector.board.id
if board in ("ODROID_M1"):
    analogIns.append((37, 0, 7))
    analogIns.append((40, 0, 6))
    alias = get_dts_alias("fe5c0000.i2c")
    if alias is not None:
        globals()[alias + "_SCL"] = GPIO3B_5
        globals()[alias + "_SDA"] = GPIO3B_6
        i2cPorts.append((int(alias[-1]), GPIO3B_5, GPIO3B_6))
    alias = get_pwm_chipid("fdd70010.pwm")
    if alias is not None:
        globals()["PWM" + alias] = GPIO0B_5
        pwmOuts.append(((int(alias[-1]), 0), GPIO0B_5))
    alias = get_pwm_chipid("fdd70020.pwm")
    if alias is not None:
        globals()["PWM" + alias] = GPIO0B_6
        pwmOuts.append(((int(alias[-1]), 0), GPIO0B_6))
    alias = get_pwm_chipid("fe6f0010.pwm")
    if alias is not None:
        globals()["PWM" + alias] = GPIO3B_2
        pwmOuts.append(((int(alias[-1]), 0), GPIO3B_2))
    alias = get_dts_alias("fdd50000.serial")
    if alias is not None:
        globals()[alias + "_TX"] = GPIO0C_1
        globals()[alias + "_RX"] = GPIO0C_0
        uartPorts.append((int(alias[-1]), GPIO0C_1, GPIO0C_0))
    alias = get_dts_alias("fe650000.serial")
    if alias is not None:
        globals()[alias + "_TX"] = GPIO3D_6
        globals()[alias + "_RX"] = GPIO3D_7
        uartPorts.append((int(alias[-1]), GPIO3D_6, GPIO3D_7))

analogIns = tuple(analogIns)
i2cPorts = tuple(i2cPorts)
pwmOuts = tuple(pwmOuts)
uartPorts = tuple(uartPorts)
