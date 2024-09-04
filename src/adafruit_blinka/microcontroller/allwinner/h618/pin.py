# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Allwinner H618 Pin Names"""
import re
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin


def find_gpiochip_number(target_label):
    """Get correct gpiochip number, legacy kernel and mainline kernel are different"""
    try:
        with open("/sys/kernel/debug/gpio", "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("The file /sys/kernel/debug/gpio does not exist.")
        return None

    gpiochip_number = None
    for line in lines:
        if target_label in line:
            match = re.search(r"gpiochip(\d+)", line)
            if match:
                gpiochip_number = match.group(1)
                break

    return gpiochip_number


if find_gpiochip_number("300b000.pinctrl"):
    __chip_num = 1
else:
    __chip_num = 0

PC0 = Pin((__chip_num, 64))
SPI0_SCLK = PC0
PC1 = Pin((__chip_num, 65))
PC2 = Pin((__chip_num, 66))
SPI0_MOSI = PC2
PC3 = Pin((__chip_num, 67))
SPI0_CS0 = PC3
PC4 = Pin((__chip_num, 68))
SPI0_MISO = PC4
PC5 = Pin((__chip_num, 69))
PC6 = Pin((__chip_num, 70))
PC7 = Pin((__chip_num, 71))
PC8 = Pin((__chip_num, 72))
PC9 = Pin((__chip_num, 73))
PC10 = Pin((__chip_num, 74))
PC11 = Pin((__chip_num, 75))
PC12 = Pin((__chip_num, 76))
PC13 = Pin((__chip_num, 77))
PC14 = Pin((__chip_num, 78))
PC15 = Pin((__chip_num, 79))

PF0 = Pin((__chip_num, 160))
PF1 = Pin((__chip_num, 161))
PF2 = Pin((__chip_num, 162))
PF3 = Pin((__chip_num, 163))
PF4 = Pin((__chip_num, 164))
PF5 = Pin((__chip_num, 165))
PF6 = Pin((__chip_num, 166))

PG0 = Pin((__chip_num, 192))
PG1 = Pin((__chip_num, 193))
PG2 = Pin((__chip_num, 194))
PG3 = Pin((__chip_num, 195))
PG4 = Pin((__chip_num, 196))
PG5 = Pin((__chip_num, 197))
PG6 = Pin((__chip_num, 198))
UART1_TX = PG6
PG7 = Pin((__chip_num, 199))
UART1_RX = PG7
PG8 = Pin((__chip_num, 200))
PG9 = Pin((__chip_num, 201))
PG10 = Pin((__chip_num, 202))
PG11 = Pin((__chip_num, 203))
PG12 = Pin((__chip_num, 204))
PG13 = Pin((__chip_num, 205))
PG14 = Pin((__chip_num, 206))
PG15 = Pin((__chip_num, 207))
TWI4_SCL = PG15
PG16 = Pin((__chip_num, 208))
TWI4_SDA = PG16
PG17 = Pin((__chip_num, 209))
TWI3_SCL = PG17
PG18 = Pin((__chip_num, 210))
TWI3_SDA = PG18
PG19 = Pin((__chip_num, 211))
PWM1 = PG19

PH0 = Pin((__chip_num, 224))
PH1 = Pin((__chip_num, 225))
PH2 = Pin((__chip_num, 226))
UART5_TX = PH2
PH3 = Pin((__chip_num, 227))
UART5_RX = PH3
PH4 = Pin((__chip_num, 228))
PH5 = Pin((__chip_num, 229))
UART2_TX = PH5
SPI1_CS0 = PH5
PH6 = Pin((__chip_num, 230))
UART2_RX = PH6
SPI1_SCLK = PH6
PH7 = Pin((__chip_num, 231))
SPI1_MOSI = PH7
PH8 = Pin((__chip_num, 232))
SPI1_MISO = PH8
PH9 = Pin((__chip_num, 233))
SPI1_CS1 = PH9
PH10 = Pin((__chip_num, 234))

PI0 = Pin((__chip_num, 256))
PI1 = Pin((__chip_num, 257))
PI2 = Pin((__chip_num, 258))
PI3 = Pin((__chip_num, 259))
PI4 = Pin((__chip_num, 260))
PI5 = Pin((__chip_num, 261))
TWI0_SCL = PI5
PI6 = Pin((__chip_num, 262))
TWI0_SDA = PI6
PI7 = Pin((__chip_num, 263))
TWI1_SCL = PI7
PI8 = Pin((__chip_num, 264))
TWI1_SDA = PI8
PI9 = Pin((__chip_num, 265))
UART3_TX = PI9
PI10 = Pin((__chip_num, 266))
UART3_RX = PI10
PI11 = Pin((__chip_num, 267))
PI12 = Pin((__chip_num, 268))
PWM2 = PI12
PI13 = Pin((__chip_num, 269))
UART4_TX = PI13
PI14 = Pin((__chip_num, 270))
UART4_RX = PI14
PI15 = Pin((__chip_num, 271))
PI16 = Pin((__chip_num, 272))

i2cPorts = (
    (0, TWI0_SCL, TWI0_SDA),
    (1, TWI1_SCL, TWI1_SDA),
    (3, TWI3_SCL, TWI3_SDA),
    (4, TWI4_SCL, TWI4_SDA),
)
# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),
    (1, SPI1_SCLK, SPI1_MOSI, SPI1_MISO),
)
# ordered as uartId, txId, rxId
uartPorts = (
    (1, UART1_TX, UART1_RX),
    (2, UART2_TX, UART2_RX),
    (3, UART3_TX, UART3_RX),
    (4, UART4_TX, UART4_RX),
    (5, UART5_TX, UART5_RX),
)

# SysFS pwm outputs, pwm channel and pin in first tuple
pwmOuts = [
    ((0, 1), PWM1),
    ((0, 2), PWM2),
]
