# SPDX-FileCopyrightText: 2024 Rippanda12
#
# SPDX-License-Identifier: MIT

"""Pin definitions for the Indiedroid Nova"""

from adafruit_blinka.microcontroller.rockchip.rk3588s import pin


# D1 = +3.3V
# D2 = +5V
D3 = pin.GPIO1_D7
# D4 = +5V
D5 = pin.GPIO1_D6
# D6 = GND
D7 = pin.GPIO1_A6
D8 = pin.GPIO4_A3
# D9 = GND
D10 = pin.GPIO4_A4
D11 = pin.GPIO1_B4
D12 = pin.GPIO0_D0
D13 = pin.GPIO1_B5
# D14 = GND
D15 = pin.GPIO3_C4
D16 = pin.GPIO3_B0
# D17 = +3.3V
D18 = pin.GPIO3_B1
D19 = pin.GPIO3_B7
# D20 = GND
D21 = pin.GPIO3_C0
D22 = pin.GPIO3_C5
D23 = pin.GPIO3_C1
D24 = pin.GPIO0_D3
# D25 = GND
D26 = pin.GPIO3_C3
D27 = pin.GPIO1_A0
D28 = pin.GPIO1_C1
D29 = pin.GPIO1_A4
# D30 = GND
D31 = pin.GPIO1_B1
D32 = pin.GPIO4_A6
D33 = pin.GPIO1_B2
# D34 = GND
D35 = pin.GPIO4_A7
D36 = pin.GPIO4_B5
D37 = pin.GPIO4_A2
D38 = pin.GPIO4_B4
# D39 = GND
D40 = pin.GPIO4_B3


# UART
# UART2_M0
UART2_TX = pin.GPIO1_B5
UART2_RX = pin.GPIO1_B6
# UART0_M2
UART0_TX = pin.GPIO4_A3
UART0_RX = pin.GPIO4_A4
# UART5_M1
UART5_TX = pin.GPIO3_C4
UART5_RX = pin.GPIO3_C5
# UART7_M1
UART7_TX = pin.GPIO3_C0
UART7_RX = pin.GPIO3_C1

# Default UART -> UART2_M0

TX = UART2_TX
RX = UART2_RX
TXD = UART2_TX
RXD = UART2_RX

# I2C

# I2C3_M1
I2C3_SCL = pin.GPIO3_B7
I2C3_SDA = pin.GPIO3_C0
# I2C5_M2
I2C5_SCL = pin.GPIO4_A6
I2C5_SDA = pin.GPIO4_A7
# I2C7_M3
I2C7_SCL = pin.GPIO4_B2
I2C7_SDA = pin.GPIO4_B3
# I2C8_M2
I2C8_SCL = pin.GPIO1_D6
I2C8_SDA = pin.GPIO1_D7

# Default I2C -> I2C8_M2
SCL = I2C8_SCL
SDA = I2C8_SDA

# SPI
# SPI0_M2
SPI0_SCLK = pin.GPIO4_A2
SPI0_MISO = pin.GPIO1_B1
SPI0_MOSI = pin.GPIO1_B2
SPI0_CS0 = pin.GPIO1_B4
# SPI1_M1
SPI1_CLK = pin.GPIO3_C1
SPI1_MISO = pin.GPIO3_C0
SPI1_MOSI = pin.GPIO3_B7
SPI1_CS1 = pin.GPIO3_C3
# SPI4_M2
SPI4_SCLK = pin.GPIO1_D6
SPI4_MISO = pin.GPIO1_D7
SPI4_MOSI = pin.GPIO1_D6
SPI4_CS0 = pin.GPIO1_D7
# SPI5_M1
SPI5_SCLK = pin.GPIO3_B1
SPI5_MISO = pin.GPIO3_B0
SPI5_MOSI = pin.GPIO3_B7
SPI5_CS1 = pin.GPIO3_C3

# Default SPI -> SPI4_M2
MOSI = SPI4_MOSI
MISO = SPI4_MISO
SCLK = SPI4_SCLK
CS = SPI4_CS0

# PWM
# PWM2_M1
PWM2 = pin.GPIO3_B1
# PWM7_M0
PWM7 = pin.GPIO0_D0
# PWM9_M0
PWM9 = pin.GPIO3_B0
# PWM11_M1
PWM11 = pin.GPIO4_B4
# PWM12_M1
PWM12 = pin.GPIO4_B5
# PWM14_M2
PWM14 = pin.GPIO1_D6
# PWM15_M0
PWM15 = pin.GPIO3_C3
