# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the ROC-RK3328-CC."""

from adafruit_blinka.microcontroller.rockchip.rk3328 import pin

for it in pin.i2cPorts:
    globals()["SCL" + str(it[0])] = it[1]
    globals()["SDA" + str(it[0])] = it[2]

SCL = pin.i2cPorts[0][1]
SDA = pin.i2cPorts[0][2]

SCLK = pin.SPI0_SCLK
MOSI = pin.SPI0_MOSI
MISO = pin.SPI0_MISO
SPI_CS = pin.SPI0_CS

# Pinout reference:
# https://github.com/libre-computer-project/libretech-wiring-tool/blob/master/libre-computer/roc-rk3328-cc/gpio.map

# 40 pin Header J1
P3 = pin.GPIO2_D1
P5 = pin.GPIO2_D0
P7 = pin.GPIO1_D4
P8 = pin.GPIO3_A4
P10 = pin.GPIO3_A6
P11 = pin.GPIO2_C4
P12 = pin.GPIO2_A6
P13 = pin.GPIO2_C5
P15 = pin.GPIO2_C6
P16 = pin.GPIO3_A7
P18 = pin.GPIO3_A5
P19 = pin.GPIO3_A1
P21 = pin.GPIO3_A2
P22 = pin.GPIO0_A2
P23 = pin.GPIO3_A0
P24 = pin.GPIO3_B0
P26 = pin.GPIO2_B4
P27 = pin.GPIO2_A4
P28 = pin.GPIO2_A5
P29 = pin.GPIO2_C3
P31 = pin.GPIO2_C7
P32 = pin.GPIO0_A0
P33 = pin.GPIO2_C0
P35 = pin.GPIO2_C2
P36 = pin.GPIO2_A0
P37 = pin.GPIO2_B7
P38 = pin.GPIO2_A1
P40 = pin.GPIO0_D3
