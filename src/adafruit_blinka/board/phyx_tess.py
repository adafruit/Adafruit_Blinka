# SPDX-FileCopyrightText: 2026 Bert Outtier
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Phyx Tess, an Adafruit Feather compatible T113-S3 board.

Names follow the silkscreen of the Feather headers, plus the usual bus names.
SPI needs a spidev device on SPI1 (/dev/spidev1.0, chip select on D10).
PWM is on F6 (PWM5), D18 (PWM2) and D19 (PWM3) once the device tree muxes
those pins to the PWM controller.
"""

from adafruit_blinka.microcontroller.allwinner.t113 import pin

# Left header
SDA = pin.PE7
SCL = pin.PE6
E12 = pin.PE12
E13 = pin.PE13
C7 = pin.PC7
F6 = pin.PF6
G11 = pin.PG11
G9 = pin.PG9
G7 = pin.PG7

# Right header
D10 = pin.PD10
TX = pin.PB4
RX = pin.PB5
MISO = CIPO = pin.PD13
MOSI = COPI = pin.PD12
SCLK = SCK = pin.PD11
D18 = pin.PD18
D19 = pin.PD19
B3 = pin.PB3
B2 = pin.PB2
G3 = pin.PG3

# A0, 0 - 1.8V
A0 = pin.GPADC0
