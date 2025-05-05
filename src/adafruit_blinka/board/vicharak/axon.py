# SPDX-FileCopyrightText: 2025 djkabutar
# See https://docs.vicharak.in/vicharak_sbcs/vaaman/vaaman-gpio-description for pinout
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Vicharak Vaaman."""

from adafruit_blinka.microcontroller.rockchip.rk3588 import pin

D2 = pin.GPIO0_B6
D4 = pin.GPIO0_B5
D9 = pin.GPIO2_C1
D10 = pin.GPIO2_B6
D11 = pin.GPIO2_C0
D12 = pin.GPIO2_B7
D13 = pin.GPIO0_C0
D17 = pin.GPIO1_D0
D18 = pin.GPIO1_D1
D19 = pin.GPIO1_D3
D20 = pin.GPIO1_D2
D23 = pin.GPIO1_B3
D29 = pin.ADC_IN1
D30 = pin.ADC_IN2
D28 = pin.ADC_IN3
D27 = pin.ADC_IN4

# UART
# UART2_M0
UART2_RX = D2
UART2_TX = D4
# UART1_M0
UART1_RX = D10
UART1_TX = D12
UART1_CSTN = D9
UART1_RSTN = D11
# UART6_M2
UART6_RX = D17
UART6_TX = D18
# UART4_M0
UART4_RX = D19
UART4_TX = D20

# Default UART -> UART2_M0
UART_RX = UART2_RX
UART_TX = UART2_TX

# I2C
# I2C2_M1
I2C2_SCL = D9
I2C2_SDA = D11
# I2C5_M4
I2C5_SCL = D10
I2C5_SDA = D12
# I2C7_M0
I2C7_SCL = D17
I2C7_SDA = D18
# I2C1_M4
I2C1_SCL = D20
I2C1_SDA = D19

# Default I2C -> I2C2_M1
SCL = I2C2_SCL
SDA = I2C2_SDA

# SPI
# SPI1_M2
SPI_MOSI = D18
SPI_MISO = D17
SPI_CLK = D20
SPI_SCLK = SPI_CLK
SPI_CS0 = D19
SPI_CS = SPI_CS0

MOSI = D18
MISO = D17
SCLK = SPI_CLK
CS = D19

# PWM
# PWM0_M1
PWM0 = D20
PWM1_M0 = D13
PWM1_M1 = D19

# ADC
ADC_IN1 = D29
ADC_IN2 = D30
ADC_IN3 = D28
ADC_IN4 = D27
