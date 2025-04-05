# SPDX-FileCopyrightText: 2025 djkabutar
# See https://docs.vicharak.in/vicharak_sbcs/vaaman/vaaman-gpio-description for pinout
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Vicharak Vaaman."""

from adafruit_blinka.microcontroller.rockchip.rk3399 import pin

D7 = pin.GPIO2_B3
D8 = pin.GPIO4_C4
D10 = pin.GPIO4_C3
D11 = pin.GPIO4_C2
D12 = pin.GPIO4_A3
D13 = pin.GPIO4_C6
D15 = pin.GPIO4_C5
D16 = pin.GPIO4_D2
D18 = pin.GPIO4_D4
D22 = pin.GPIO4_D5
D27 = pin.GPIO2_A0
D28 = pin.GPIO2_A1
D29 = pin.GPIO2_B2
D31 = pin.GPIO2_B1
D32 = pin.GPIO3_C0
D33 = pin.GPIO2_B4
D35 = pin.GPIO4_A5
D36 = pin.GPIO4_A4
D37 = pin.GPIO4_D6
D38 = pin.GPIO4_A6
D40 = pin.GPIO4_A7

SDA2 = D27
SCL2 = D28

SDA6 = D31
SCL6 = D29

SDA7 = pin.I2C7_SDA
SCL7 = pin.I2C7_SCL

SDA = SDA2
SCL = SCL2

UART2_TX = D8
UART2_RX = D10

UART_TX = UART2_TX
UART_RX = UART2_RX

PWM0 = pin.PWM0
PWM1 = pin.PWM1

ADC_IN0 = pin.ADC_IN0
