# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the AML-S905X-CC-V1."""

from adafruit_blinka.microcontroller.amlogic.s905x import pin

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
# https://github.com/libre-computer-project/libretech-wiring-tool/blob/master/libre-computer/aml-s905x-cc/gpio.map

# 40 pin Header 7J1
P3 = pin.GPIO105
P5 = pin.GPIO104
P7 = pin.GPIO289
P8 = pin.GPIO291
P10 = pin.GPIO292
P12 = pin.GPIO106
P13 = pin.GPIO109
P15 = pin.GPIO110
P16 = pin.GPIO293
P18 = pin.GPIO294
P19 = pin.GPIO287
P21 = pin.GPIO288
P22 = pin.GPIO279
P23 = pin.GPIO290
P24 = pin.GPIO289
P26 = pin.GPIO280
P27 = pin.GPIO275
P28 = pin.GPIO276
P29 = pin.GPIO296
P31 = pin.GPIO297
P32 = pin.GPIO295
P33 = pin.GPIO285
P35 = pin.GPIO286
P36 = pin.GPIO281
P37 = pin.GPIO284
P38 = pin.GPIO282
P40 = pin.GPIO283

# 8 Pin Header 2J3
P2J33 = pin.GPIO225
P2J34 = pin.GPIO224
P2J35 = pin.GPIO223
P2J36 = pin.GPIO222

# 3 Pin Header 2J1
P2J12 = pin.GPIO100
P2J13 = pin.GPIO101

# 3 Pin Header 9J1
P9J12 = pin.GPIO220
