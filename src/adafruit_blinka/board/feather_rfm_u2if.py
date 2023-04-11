# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Pin definitions for the Feather RP2040 RFM with u2if firmware.

Adafruit CircuitPython 6.2.0 on 2021-04-05; Adafruit Feather RP2040 RFM with rp2040
>>> import board
>>> board.
A0              A1              A2              A3
D0              D1              D10             D11
D12             D13             D24             D25
D4              D5              D6              D9
I2C             SDA             SCL             LED
NEOPIXEL        SPI             SCK             MISO
MOSI            RX              TX              UART
RFM_CS          RFM_RST         RFM_IO5         RFM_IO3
RFM_IO4         RFM_IO0         RFM_IO1         RFM_IO2
"""

from adafruit_blinka.microcontroller.rp2040_u2if import pin

D0 = RX = pin.GP1
D1 = TX = pin.GP0
D4 = pin.GP4
D5 = pin.GP5
D6 = pin.GP6
D9 = pin.GP9
D10 = pin.GP10
D11 = pin.GP11
D12 = pin.GP12
D13 = pin.GP13
D24 = pin.GP24
D25 = pin.GP25

A0 = pin.GP26
A1 = pin.GP27
A2 = pin.GP28
A3 = pin.GP29

LED = pin.GP13

BUTTON = BOOT = pin.GP7

NEOPIXEL = pin.GP4

SDA = pin.GP2
SCL = pin.GP3

SCLK = SCK = pin.GP14
MOSI = pin.GP15
MISO = pin.GP8

RFM_CS = pin.GP16
RFM_RST = pin.GP17
RFM_IO5 = pin.GP18
RFM_IO3 = pin.GP19
RFM_IO4 = pin.GP20
RFM_IO0 = pin.GP21
RFM_IO1 = pin.GP22
RFM_IO2 = pin.GP23

# access u2if via pin instance to open for specifc VID/PID
# pylint:disable = protected-access
pin.GP0._u2if_open_hid(0x239A, 0x812E)
