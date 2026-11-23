# SPDX-FileCopyrightText: 2026 Bert Outtier
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Phyx Tess, an Adafruit Feather compatible T113-S3 board.

The Feather names (D5 to D13, A0 to A5 and the bus names) are on the pins
a Feather has there, so FeatherWing code works as written. The silkscreen
names the header pins after their T113 port (E12, F6, D18, ...): those
names work too, except for "D10" on the silkscreen, which is PD10, the SPI1
chip select, here CE0, as board.D10 is the Feather D10, PF6.
SPI needs a spidev device on SPI1 (/dev/spidev1.0, chip select CE0).
PWM is on D10 (F6, PWM5), A5 (D18, PWM2) and A4 (D19, PWM3) once the device
tree muxes those pins to the PWM controller. LED is user LED 0 (PG14),
active low, once the device tree leaves it to user space instead of the
Linux LED driver.
"""

from adafruit_blinka.microcontroller.allwinner.t113 import pin

# 12-pin side of the Feather header
SDA = pin.PE7
SCL = pin.PE6
D5 = E12 = pin.PE12
D6 = E13 = pin.PE13
D9 = C7 = pin.PC7
D10 = F6 = pin.PF6
D11 = G11 = pin.PG11
D12 = G9 = pin.PG9
D13 = G7 = pin.PG7

# 16-pin side of the Feather header
CE0 = pin.PD10
TX = pin.PB4
RX = pin.PB5
MISO = CIPO = pin.PD13
MOSI = COPI = pin.PD12
SCLK = SCK = pin.PD11
A5 = D18 = pin.PD18
A4 = D19 = pin.PD19
A3 = B3 = pin.PB3
A2 = B2 = pin.PB2
A1 = G3 = pin.PG3

# A0, 0 - 1.8V, the only analog input (A1 to A5 are digital only)
A0 = pin.GPADC0

# User LED 0, active low
LED = pin.PG14
