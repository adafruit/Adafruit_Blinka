# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the NanoPi NEO Air."""
# Enable I2C0, UART1, and SPI by adding the following lines to /boot/armbianEnv.txt
#    overlays=usbhost2 usbhost3 spi-spidev uart1 i2c0
#    param_spidev_spi_bus=0

from adafruit_blinka.microcontroller.allwinner.h3 import pin

# Left GPIOs
D2 = pin.PA12
D3 = pin.PA11
D4 = pin.PG11
D17 = pin.PA0
D27 = pin.PA2
D22 = pin.PA3
D10 = pin.PC0
D9 = pin.PC1
D11 = pin.PC2

# Right GPIOs
D14 = pin.PG6
D15 = pin.PG7
D18 = pin.PA6
D23 = pin.PG8
D24 = pin.PG9
D25 = pin.PA1
D8 = pin.PC3

# I2C
SDA = D2
SCL = D3

# SPI
SCLK = D11
MOSI = D10
MISO = D9
CE0 = D8
SCK = SCLK

# Serial UART
UART1_TX = D14
UART1_RX = D15

UART2_RX = D8
UART2_TX = D17
UART2_RTS = D27
UART2_CTS = D22

# PWM
PWM1 = D4
