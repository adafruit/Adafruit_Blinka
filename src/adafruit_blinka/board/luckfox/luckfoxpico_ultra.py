# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Luckfox Pico Ultra."""

from adafruit_blinka.microcontroller.rockchip.rv1106 import pin

G32 = pin.GPIO1_A0
G33 = pin.GPIO1_A1
G40 = pin.GPIO1_B0
G41 = pin.GPIO1_B1
G42 = pin.GPIO1_B2
G43 = pin.GPIO1_B3
G48 = pin.GPIO1_C0
G49 = pin.GPIO1_C1
G50 = pin.GPIO1_C2
G51 = pin.GPIO1_C3
G52 = pin.GPIO1_C4
G53 = pin.GPIO1_C5
G54 = pin.GPIO1_C6
G55 = pin.GPIO1_C7
G56 = pin.GPIO1_D0
G57 = pin.GPIO1_D1
G58 = pin.GPIO1_D2
G59 = pin.GPIO1_D3
G64 = pin.GPIO2_A0
G65 = pin.GPIO2_A1
G66 = pin.GPIO2_A2
G67 = pin.GPIO2_A3
G68 = pin.GPIO2_A4
G69 = pin.GPIO2_A5
G70 = pin.GPIO2_A6
G71 = pin.GPIO2_A7
G72 = pin.GPIO2_B0
G73 = pin.GPIO2_B1
G144 = pin.GPIO4_C0
G145 = pin.GPIO4_C1

# UART
UART3_TX = pin.UART3_TX_M1
UART3_RX = pin.UART3_RX_M1
UART4_TX = pin.UART4_TX_M1
UART4_RX = pin.UART4_RX_M1

# Default UART
TX = UART3_TX
RX = UART3_RX
TXD = UART3_TX
RXD = UART3_RX

# I2C
I2C3_SCL = pin.I2C3_SCL_M1
I2C3_SDA = pin.I2C3_SDA_M1

# Default I2C
SCL = I2C3_SCL
SDA = I2C3_SDA

# SPI
SPI0_MISO = pin.SPI0_MISO_M0
SPI0_MOSI = pin.SPI0_MOSI_M0
SPI0_SCLK = pin.SPI0_CLK_M0
SPI0_CS0 = pin.SPI0_CS0_M0
SPI0_CS1 = pin.SPI0_CS1_M0

# Default SPI
MISO = SPI0_MISO
MOSI = SPI0_MOSI
SCLK = SPI0_SCLK

# PWM
PWM5 = pin.PWM5
PWM6 = pin.PWM6
PWM10 = pin.PWM10
PWM11 = pin.PWM11

# ADC
ADC_IN0 = pin.ADC_IN0
ADC_IN1 = pin.ADC_IN1
