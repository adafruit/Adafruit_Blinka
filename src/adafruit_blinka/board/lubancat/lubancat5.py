# SPDX-FileCopyrightText: 2024 mmontol
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the LubanCat-5."""

from adafruit_blinka.microcontroller.rockchip.rk3588 import pin
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# GPIO1 = +3.3V
# GPIO2 = +5V
GPIO3 = pin.GPIO1_C0
# GPIO4 = +5V
GPIO5 = pin.GPIO1_C1
# GPIO6 = GND
GPIO7 = Pin((6, 0))
GPIO8 = pin.GPIO1_B6
# GPIO9 = GND
GPIO10 = pin.GPIO1_B7
GPIO11 = Pin((6, 1))
GPIO12 = Pin((6, 4))
GPIO13 = Pin((6, 2))
# GPIO14 = GND
GPIO15 = Pin((6, 3))
GPIO16 = Pin((6, 5))
# GPIO17 = +3.3V
GPIO18 = Pin((6, 6))
GPIO19 = pin.GPIO4_A1
# GPIO20 = GND
GPIO21 = pin.GPIO4_A0
GPIO22 = Pin((6, 7))
GPIO23 = pin.GPIO4_A2
GPIO24 = pin.GPIO4_B2
# GPIO25 = GND
GPIO26 = Pin((7, 5))
GPIO27 = pin.GPIO1_A2
GPIO28 = pin.GPIO1_A3
GPIO29 = pin.GPIO2_C3
# GPIO30 = GND
GPIO31 = Pin((7, 0))
GPIO32 = pin.GPIO4_B6
GPIO33 = pin.GPIO1_D6
# GPIO34 = GND
GPIO35 = pin.GPIO1_D7
GPIO36 = Pin((7, 4))
GPIO37 = Pin((7, 1))
GPIO38 = Pin((7, 3))
# GPIO39 = GND
GPIO40 = Pin((7, 2))

# I2C
I2C3_SCL = pin.I2C3_SCL_M0
I2C3_SDA = pin.I2C3_SDA_M0
I2C4_SCL = pin.I2C4_SCL_M3
I2C4_SDA = pin.I2C4_SDA_M3
I2C8_SCL = pin.I2C8_SCL_M2
I2C8_SDA = pin.I2C8_SDA_M2

# UART
UART1_TX = pin.UART1_TX_M1
UART1_RX = pin.UART1_RX_M1
UART3_TX = pin.UART3_TX_M0
UART3_RX = pin.UART3_RX_M0

# Default SPI
MOSI = pin.SPI0_MOSI_M1
MISO = pin.SPI0_MISO_M1
SCLK = pin.SPI0_SCLK_M1
CS0 = pin.SPI0_CS0_M1

# PWM
PWM0 = pin.PWM0_M2
PWM1 = pin.PWM1_M2
PWM13_M1 = pin.PWM13_M1
PWM13_M2 = pin.PWM13_M2
PWM14_M1 = pin.PWM14_M1
PWM14_M2 = pin.PWM14_M2
PWM15 = pin.PWM15_IR_M3
