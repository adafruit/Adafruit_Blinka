# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Odyssey X86j41X5."""

from adafruit_blinka.microcontroller.pentium.j4105 import pin

D0 = pin.GPIO388
D1 = pin.GPIO389
D2 = pin.GPIO386
D3 = pin.GPIO387
D4 = pin.GPIO337
D5 = pin.GPIO415
D6 = pin.GPIO416
D7 = pin.GPIO357
D8 = pin.GPIO356
D9 = pin.GPIO358
D10 = pin.GPIO359
D11 = pin.GPIO355
D12 = pin.GPIO391
D13 = pin.GPIO417
D14 = pin.GPIO493
D15 = pin.GPIO492
D16 = pin.GPIO410
D17 = pin.GPIO364
D18 = pin.GPIO338
D19 = pin.GPIO339
D20 = pin.GPIO340
D21 = pin.GPIO341
D22 = pin.GPIO413
D23 = pin.GPIO421
D24 = pin.GPIO422
D25 = pin.GPIO390
D26 = pin.GPIO419
D27 = pin.GPIO412

SDA = D2
SCL = D3

SCL2 = D1
SDA2 = D0

SCLK = D11
MOSI = D10
MISO = D9
CS = D8
SCK = SCLK

UART_TX = D14
UART_RX = D15
