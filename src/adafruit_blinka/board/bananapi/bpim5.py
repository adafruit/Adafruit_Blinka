# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Banana Pi M5."""

from adafruit_blinka.microcontroller.amlogic.s905x3 import pin

for it in pin.i2cPorts:
    globals()["SCL" + str(it[0])] = it[1]
    globals()["SDA" + str(it[0])] = it[2]

SCL = pin.i2cPorts[0][1]
SDA = pin.i2cPorts[0][2]

SCLK = pin.SPI0_SCLK
MOSI = pin.SPI0_MOSI
MISO = pin.SPI0_MISO
SPI_CS0 = pin.SPI0_CS0

# Pinout reference:
# https://wiki.banana-pi.org/Banana_Pi_BPI-M5#BPI-M5_40PIN_GPIO_.28CON2.29
P3 = pin.GPIOX_17   # I2C_M2_SDA
P5 = pin.GPIOX_18   # I2C_M2_SCL
P7 = pin.GPIOX_5    # Verified
P8 = pin.GPIOX_12   # UART_A_TX
P10 = pin.GPIOX_13  # UART_A_RX
P11 = pin.GPIOX_3   # Verified
P12 = pin.GPIOA_8   # TDMB_SCLK
P13 = pin.GPIOX_4   # Verified
P15 = pin.GPIOX_7   # Verified
P16 = pin.GPIOX_0   # Verified
P18 = pin.GPIOX_1   # Verified
P19 = pin.GPIOX_8   # PCM_DIN
P21 = pin.GPIOX_9   # PCM_DOUT
P22 = pin.GPIOX_2   # SDIO_D2
P23 = pin.GPIOX_11  # PCM_CLK
P24 = pin.GPIOX_10  # PCM_SYNC
P26 = pin.GPIOX_16  # Verified
P27 = pin.GPIOA_14  # Verified
P28 = pin.GPIOA_15  # Verified
P29 = pin.GPIOX_14  # Verified
P31 = pin.GPIOX_15  # Verified
P32 = pin.GPIOX_19  # Verified
P33 = pin.GPIOX_6   # Verified
P35 = pin.GPIOAO_7  # Verified
P36 = pin.GPIOH_5   # Verified
P37 = pin.GPIOAO_7  # I2S_MCLK
P38 = pin.GPIOAO_10 # TDMB_DIN SPDIF_OUT
P40 = pin.GPIOAO_4  # TDMB_DOUT
