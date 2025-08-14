# SPDX-FileCopyrightText: 2025 Brett Walach for Particle
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Tachyon."""

from adafruit_blinka.microcontroller.quectel.qcm6490 import pin

for it in pin.i2cPorts:
    globals()["SCL" + str(it[0])] = it[1]
    globals()["SDA" + str(it[0])] = it[2]

SCL = pin.i2cPorts[0][1]
SDA = pin.i2cPorts[0][2]

D0 = pin.GPIO_36
D1 = pin.GPIO_37
D2 = pin.GPIO_8
D3 = pin.GPIO_9
D4 = pin.GPIO_61
D5 = pin.GPIO_18
D6 = pin.GPIO_19
D7 = pin.GPIO_62
D8 = pin.GPIO_59
D9 = pin.GPIO_56
D10 = pin.GPIO_57
D11 = pin.GPIO_58
D12 = pin.GPIO_78
D13 = pin.GPIO_106
D14 = pin.GPIO_34
D15 = pin.GPIO_35
D16 = pin.GPIO_32
D17 = pin.GPIO_33
D18 = pin.GPIO_144
D19 = pin.GPIO_145
D20 = pin.GPIO_146
D21 = pin.GPIO_147
D22 = pin.GPIO_158
D23 = pin.GPIO_165
D24 = pin.GPIO_166
D25 = pin.GPIO_24
D26 = pin.GPIO_6
D27 = pin.GPIO_44

CS = D8
MISO = D9
MOSI = D10
SCLK = D11
SCK = SCLK

UART_TX = D14
UART_RX = D15

PWM1 = D13
