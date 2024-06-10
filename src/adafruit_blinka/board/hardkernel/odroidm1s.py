# SPDX-FileCopyrightText: 2023 Steve Jeong for Hardkernel
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Odroid M1S."""

from adafruit_blinka.microcontroller.rockchip.rk3566 import pin

D8 = pin.GPIO2_A4
D10 = pin.GPIO2_A3
D12 = pin.GPIO2_A7
D16 = pin.GPIO2_B5
D18 = pin.GPIO2_B6
D22 = pin.GPIO2_B0
D24 = pin.GPIO3_A1
D26 = pin.GPIO2_B1
D28 = pin.GPIO0_B3
D32 = pin.GPIO2_B2
D36 = pin.GPIO2_A6
D3 = pin.GPIO3_B6
D5 = pin.GPIO3_B5
D7 = pin.GPIO0_B6
D11 = pin.GPIO0_C0
D13 = pin.GPIO0_C1
D15 = pin.GPIO0_C2
D19 = pin.GPIO3_C1
D21 = pin.GPIO3_C2
D23 = pin.GPIO3_C3
D27 = pin.GPIO0_B4
D29 = pin.GPIO2_C0
D31 = pin.GPIO2_B7
D33 = pin.GPIO0_B5
D35 = pin.GPIO2_A5

# external pins
EXT_D11 = pin.GPIO3_C4
EXT_D12 = pin.GPIO3_C5
EXT_D13 = pin.GPIO3_B3
EXT_D14 = pin.GPIO3_B4

SDA = D3
SCL = D5

SCLK = D23
MOSI = D19
MISO = D21
CS0 = D24
CS1 = D26
CS = CS0  # aliased for backward compatibility

UART0_TX = D8
UART0_RX = D10
UART1_TX = D13
UART1_RX = D11

UART1_CTS = D29
UART1_RTS = D31

I2C0_SDA = D3
I2C0_SCL = D5
I2C1_SDA = D27
I2C1_SCL = D28

""" ADC """
A0 = 40
A1 = 37

""" PWM """
PWM = D15
