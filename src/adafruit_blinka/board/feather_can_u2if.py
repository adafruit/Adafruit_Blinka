# SPDX-FileCopyrightText: 2023 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Pin definitions for the Feather RP2040 CAN with u2if firmware.

Adafruit CircuitPython 6.2.0 on 2021-04-05; Adafruit Feather RP2040 CAN with rp2040
>>> import board
>>> board.
A0              A1              A2              A3
D0              D1              D10             D11
D12             D13             D24             D25
D4              D5              D6              D9
I2C             SDA             SCL             LED
NEOPIXEL        SPI             SCK             MISO
MOSI            RX              TX              UART
CAN_STANDBY     CAN_TX0_RTS     CAN_RESET       CAN_CS
CAN_INTERRUPT   CAN_RX0_BF      NEOPIXEL_POWER
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

NEOPIXEL = pin.GP21
NEOPIXEL_POWER = pin.GP20

SDA = pin.GP2
SCL = pin.GP3

SCLK = SCK = pin.GP14
MOSI = pin.GP15
MISO = pin.GP8

CAN_STANDBY = pin.GP16
CAN_TX0_RTS = pin.GP17
CAN_RESET = pin.GP18
CAN_CS = pin.GP19
CAN_INTERRUPT = pin.GP22
CAN_RX0_BF = pin.GP23

# access u2if via pin instance to open for specifc VID/PID
# pylint:disable = protected-access
pin.GP0._u2if_open_hid(0x239A, 0x8130)
