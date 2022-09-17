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
P3 = pin.GPIOX_17  # I2C_M2_SDA
P5 = pin.GPIOX_18  # I2C_M2_SCL
P7 = pin.GPIOX_5
P8 = pin.GPIOX_12  # UART_A_TX
P10 = pin.GPIOX_13  # UART_A_RX
P11 = pin.GPIOX_3
P12 = pin.GPIOA_8  # TDMB_SCLK
P13 = pin.GPIOX_4
P15 = pin.GPIOX_7
P16 = pin.GPIOX_0
P18 = pin.GPIOX_1
P19 = pin.GPIOX_8  # PCM_DIN
P21 = pin.GPIOX_9  # PCM_DOUT
P22 = pin.GPIOX_2  # SDIO_D2
P23 = pin.GPIOX_11  # PCM_CLK
P24 = pin.GPIOX_10  # PCM_SYNC
P26 = pin.GPIOX_16  # PWM_E
P27 = pin.GPIOA_14  # I2C_M3_SDA
P28 = pin.GPIOA_15  # I2C_M3_SCL
P29 = pin.GPIOX_14  # UART_A_CTS
P31 = pin.GPIOX_15  # UART_A_RTS
P32 = pin.GPIOX_19  # PWM_B
P33 = pin.GPIOX_6
P35 = pin.GPIOAO_7  # TDMB_FS
P36 = pin.GPIOH_5
P37 = pin.GPIOAO_9  # I2S_MCLK
P38 = pin.GPIOAO_10  # TDMB_DIN SPDIF_OUT
P40 = pin.GPIOAO_4  # TDMB_DOUT
