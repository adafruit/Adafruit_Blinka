# SPDX-FileCopyrightText: 2024 cst_zf
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Orangepi 3B."""

from adafruit_blinka.microcontroller.rockchip.rk3566 import pin

# D pin number is ordered by physical pin sequence
# Reference: https://service.robots.org.nz/wiki/Wiki.jsp?page=OrangePi

# D2 = VCC5V0_SYS
D3 = pin.I2C2_SDA_M1
# D4 = VCC5V0_SYS
D5 = pin.I2C2_SCL_M1
# D6 = GND
D7 = pin.GPIO4_C3  # GPIO4_C3/PWM15
D8 = pin.GPIO0_D1
# D9 = GND
D10 = pin.GPIO0_D0
D11 = pin.GPIO3_C6
D12 = pin.GPIO3_C7
D13 = pin.GPIO4_A0
# D14 = GND
D15 = pin.GPIO4_A2
D16 = pin.GPIO4_A3
# D17 = Vcc3V3_SYS
D18 = pin.GPIO4_A1
D19 = pin.SPI3_MOSI_M0
# D20 = GND
D21 = pin.SPI3_MISO_M0
D22 = pin.GPIO4_A4
D23 = pin.SPI3_CLK_M0
D24 = pin.SPI3_CS0_M0
# D25 = GND
D26 = pin.GPIO4_A7
D27 = pin.I2C3_SDA_M0
D28 = pin.I2C3_SCL_M0
D29 = pin.GPIO4_A5
# D30 = GND
D31 = pin.GPIO3_D4
D32 = pin.GPIO4_C0
D33 = pin.GPIO3_D7
# D34 = GND
D35 = pin.GPIO3_D0
D36 = pin.GPIO3_D5
D37 = pin.GPIO3_D3
D38 = pin.GPIO3_D2
# D39 = GND
D40 = pin.GPIO3_D1

# UART
UART2_TX_M0 = pin.GPIO0_D1
UART2_RX_M0 = pin.GPIO0_D0

UART7_TX_M2 = pin.GPIO4_A2
UART7_RX_M2 = pin.GPIO4_A3

UART3_TX_M0 = pin.GPIO1_A1
UART3_RX_M0 = pin.GPIO1_A0

UART9_TX_M2 = pin.GPIO4_A4
UART9_RX_M2 = pin.GPIO4_A5

# I2C
I2C2_SCL_M1 = pin.I2C2_SCL_M1
I2C2_SDA_M1 = pin.I2C2_SDA_M1
I2C3_SCL_M0 = pin.I2C3_SCL_M0
I2C3_SDA_M0 = pin.I2C3_SDA_M0

# Default I2C
SCL = I2C2_SCL_M1
SDA = I2C2_SDA_M1

# SPI
SPI3_MISO = pin.SPI3_MISO_M0
SPI3_MOSI = pin.SPI3_MOSI_M0
SPI3_CLK = pin.SPI3_CLK_M0
SPI3_CS0 = pin.SPI3_CS0_M0

# Default SPI
MOSI = SPI3_MOSI
MISO = SPI3_MISO
SCLK = SPI3_CLK
CS = SPI3_CS0
