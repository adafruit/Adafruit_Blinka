# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
# See https://wiki.radxa.com/Rock4/hardware/gpio for pinout
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Vivid Unit Board. Pins are
BCM Equivalent GPIO numbers rather than phyisical pin numbers."""

from adafruit_blinka.microcontroller.rockchip.rk3399 import pin

D0 = pin.GPIO2_A7
D1 = pin.GPIO2_B0
D2 = pin.GPIO2_A0
D3 = pin.GPIO2_A1
D4 = pin.GPIO4_D1
D5 = pin.GPIO1_A4
D6 = pin.GPIO1_A2
D7 = pin.GPIO2_A5
D8 = pin.GPIO2_B4
D9 = pin.GPIO2_B1
D10 = pin.GPIO2_B2
D11 = pin.GPIO2_B3
D12 = pin.GPIO1_A1
D13 = pin.GPIO4_B3
D14 = pin.GPIO4_C4
D15 = pin.GPIO4_C3
D16 = pin.GPIO4_B4
D17 = pin.GPIO4_D6
D18 = pin.GPIO4_D2
D19 = pin.GPIO4_B5
D20 = pin.GPIO4_B1
D21 = pin.GPIO4_B2
D22 = pin.GPIO2_A4
D23 = pin.GPIO2_A6
D24 = pin.GPIO2_A3
D25 = pin.GPIO2_A2
D26 = pin.GPIO4_B0
D27 = pin.GPIO2_D3

SDA = D2
SCL = D3

SCLK = D11
MOSI = D10
MISO = D9
CS = D8
SCK = SCLK

UART2_TX = D14
UART2_RX = D15

UART4_TX = D10
UART4_RX = D9

UART_TX = UART2_TX
UART_RX = UART2_RX

PWM0 = pin.PWM0
PWM1 = pin.PWM1

ADC_IN0 = pin.ADC_IN0
ADC_IN3 = pin.ADC_IN3
ADC_IN4 = pin.ADC_IN4
