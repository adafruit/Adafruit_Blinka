# SPDX-FileCopyrightText: 2022 MrPanc0 for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Odroid M1."""

from adafruit_blinka.microcontroller.rockchip.rk3568b2 import pin

D8 = pin.GPIO3D_6
D10 = pin.GPIO3D_7
D12 = pin.GPIO3D_0
D16 = pin.GPIO3C_6
D18 = pin.GPIO3D_7
D22 = pin.GPIO3D_1
D24 = pin.GPIO2D_2
D26 = pin.GPIO3D_2
D28 = pin.GPIO0B_3
D32 = pin.GPIO3D_3
D36 = pin.GPIO3D_4
D3 = pin.GPIO3B_6
D5 = pin.GPIO3B_5
D7 = pin.GPIO0B_6
D11 = pin.GPIO0C_0
D13 = pin.GPIO0C_1
D15 = pin.GPIO3B_2
D19 = pin.GPIO2D_1
D21 = pin.GPIO2D_0
D23 = pin.GPIO2D_3
D27 = pin.GPIO0B_4
D29 = pin.GPIO4C_1
D31 = pin.GPIO4B_6
D33 = pin.GPIO0B_5
D35 = pin.GPIO3D_5

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
