# SPDX-FileCopyrightText: 2024 Chris Brown
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Pine64 Quartz64 Model A."""

from adafruit_blinka.microcontroller.rockchip.rk3566 import pin

I2C3_SDA_M0 = pin.I2C3_SDA_M0
I2C3_SCL_M0 = pin.I2C3_SCL_M0
UART2_TX_M0_DEBUG = pin.UART2_TX
UART2_RX_M0_DEBUG = pin.UART2_RX
SPI1_MOSI_M1 = pin.SPI1_MOSI_M1
SPI1_MISO_M1 = pin.SPI1_MISO_M1
SPI1_CLK_M1 = pin.SPI1_CLK_M1
SPI1_CS0_M1 = pin.SPI1_CS0_M1
UART0_TX = pin.UART0_TX
UART0_RX = pin.UART0_RX
CPU_REFCLK_OUT = pin.CPU_REFCLK_OUT

# Default UART
TX = UART0_TX
RX = UART0_RX

# Default I2C
SCL = I2C3_SCL_M0
SDA = I2C3_SDA_M0

# Default SPI
SCLK = SPI1_CLK_M1
MOSI = SPI1_MOSI_M1
MISO = SPI1_MISO_M1
CS = SPI1_CS0_M1
