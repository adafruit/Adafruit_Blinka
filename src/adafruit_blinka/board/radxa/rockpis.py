# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Rock Pi S."""

from adafruit_blinka.microcontroller.rockchip.rk3308 import pin

D2 = pin.GPIO0_B3
D3 = pin.GPIO0_B4
D4 = pin.GPIO2_A4
D8 = pin.GPIO1_D1
D9 = pin.GPIO1_C6
D10 = pin.GPIO1_C7
D11 = pin.GPIO1_D0
D14 = pin.GPIO2_A1
D15 = pin.GPIO2_A0
D17 = pin.GPIO0_B7
D18 = pin.GPIO2_A5
D22 = pin.GPIO0_C1
D23 = pin.GPIO2_B2
D24 = pin.GPIO2_B1
D25 = pin.GPIO2_A7
D27 = pin.GPIO0_C0

SDA0 = pin.I2C0_SDA
SCL0 = pin.I2C0_SCL

SDA1 = pin.I2C1_SDA
SCL1 = pin.I2C1_SCL

SCL2 = pin.I2C2_SCL
SDA2 = pin.I2C2_SDA

SCL3 = pin.I2C3_SCL
SDA3 = pin.I2C3_SDA

SDA = SDA1
SCL = SCL1

SCLK = pin.SPI2_SCLK
MOSI = pin.SPI2_MOSI
MISO = pin.SPI2_MISO
CS = pin.SPI2_CS
SCK = SCLK

UART_TX = pin.UART0_TX
UART_RX = pin.UART0_RX

UART1_TX = pin.UART1_TX
UART1_RX = pin.UART1_RX

UART2_TX = pin.UART2_TX
UART2_RX = pin.UART2_RX

PWM2 = pin.PWM2
PWM3 = pin.PWM3

ADC_IN0 = pin.ADC_IN0
