# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Orangepi 4."""

from adafruit_blinka.microcontroller.rockchip.rk3399 import pin

# D pin number is ordered by physical pin sequence
# Reference: https://service.robots.org.nz/wiki/Wiki.jsp?page=OrangePi

# +------+-----+----------+------+---+OrangePi 4+---+---+--+----------+-----+------+
# | GPIO | wPi |   Name   | Mode | V | Physical | V | Mode | Name     | wPi | GPIO |
# +------+-----+----------+------+---+----++----+---+------+----------+-----+------+
# |      |     |     3.3V |      |   |  1 || 2  |   |      | 5V       |     |      |
# |   64 |   0 | I2C2_SDA |   IN | 1 |  3 || 4  |   |      | 5V       |     |      |
# |   65 |   1 | I2C2_SCL |   IN | 1 |  5 || 6  |   |      | GND      |     |      |
# |  150 |   2 |     PWM1 | ALT2 | 1 |  7 || 8  | 1 | ALT2 | I2C3_SCL | 3   | 145  |
# |      |     |      GND |      |   |  9 || 10 | 1 | ALT2 | I2C3_SDA | 4   | 144  |
# |   33 |   5 | GPIO1_A1 |   IN | 0 | 11 || 12 | 1 | IN   | GPIO1_C2 | 6   | 50   |
# |   35 |   7 | GPIO1_A3 |  OUT | 1 | 13 || 14 |   |      | GND      |     |      |
# |   92 |   8 | GPIO2_D4 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO1_C6 | 9   | 54   |
# |      |     |     3.3V |      |   | 17 || 18 | 0 | IN   | GPIO1_C7 | 10  | 55   |
# |   40 |  11 | SPI1_TXD | ALT3 | 0 | 19 || 20 |   |      | GND      |     |      |
# |   39 |  12 | SPI1_RXD | ALT3 | 1 | 21 || 22 | 0 | IN   | GPIO1_D0 | 13  | 56   |
# |   41 |  14 | SPI1_CLK | ALT3 | 1 | 23 || 24 | 1 | ALT3 | SPI1_CS  | 15  | 42   |
# |      |     |      GND |      |   | 25 || 26 | 0 | IN   | GPIO4_C5 | 16  | 149  |
# |   64 |  17 | I2C2_SDA |   IN | 1 | 27 || 28 | 1 | IN   | I2C2_SCL | 18  | 65   |
# |      |     |  I2S0_RX |      |   | 29 || 30 |   |      | GND      |     |      |
# |      |     |  I2S0_TX |      |   | 31 || 32 |   |      | I2S_CLK  |     |      |
# |      |     | I2S0_SCK |      |   | 33 || 34 |   |      | GND      |     |      |
# |      |     | I2S0_SI0 |      |   | 35 || 36 |   |      | I2S0_SO0 |     |      |
# |      |     | I2S0_SI1 |      |   | 37 || 38 |   |      | I2S0_SI2 |     |      |
# |      |     |      GND |      |   | 39 || 40 |   |      | I2S0_SI3 |     |      |
# +------+-----+----------+------+---+----++----+---+------+----------+-----+------+
# | GPIO | wPi |   Name   | Mode | V | Physical | V | Mode | Name     | wPi | GPIO |
# +------+-----+----------+------+---+OrangePi 4+---+---+--+----------+-----+------+

# D1 = VCC3V3_SYS
# D2 = VCC5V0_SYS
D3 = pin.I2C2_SDA  # I2C2_SDA_3V0
# D4 = VCC5V0_SYS
D5 = pin.I2C2_SCL  # I2C2_SCL_3V0
# D6 = GND
D7 = pin.GPIO4_C6  # GPIO4_C6/PWM1
D8 = pin.I2C3_SCL  # I2C3_SCL
# D9 = GND
D10 = pin.I2C3_SDA  # I2C3_SDA
D11 = pin.GPIO1_A1  # GPIO1_A1
D12 = pin.GPIO1_C2  # GPIO1_C2
D13 = pin.GPIO1_A3  # GPIO1_A3
# D14 = GND
D15 = pin.GPIO2_D4  # GPIO2_D4
D16 = pin.GPIO1_C6  # GPIO1_C6
# D17 = GND
D18 = pin.GPIO1_C7  # GPIO1_C7
D19 = pin.GPIO1_B0  # UART4_TX / SPI1_TXD
# D20 = GND
D21 = pin.GPIO1_A7  # UART4_RX / SPI1_RXD
D22 = pin.GPIO1_D0  # GPIO1_D0
D23 = pin.GPIO1_B1  # SPI1_CLK
D24 = pin.GPIO1_B2  # SPI1_CSn0
# D25 = GND
D26 = pin.GPIO4_C5  # GPIO4_C5
D27 = pin.I2C2_SDA  # I2C2_SDA
D28 = pin.I2C2_SCL  # I2C2_SCL
# D29 = pin.I2S0_LRCK_RX
# D30 = GND
# D31 = pin.I2S0_LRCK_TX
# D32 = pin.I2S_CLK
# D33 = pin.I2S0_SCLK
# D34 = GND
# D35 = pin.I2S0_SDI0
# D36 = pin.I2S0_SDO0
# D37 = pin.I2S0_SDI1SDO_3
# D38 = pin.I2S0_SDI2SDO2
# D39 = GND
# D40 = pin.I2S0_SDI3SDO1

# UART
UART4_TX = pin.GPIO1_B0
UART4_RX = pin.GPIO1_A7
