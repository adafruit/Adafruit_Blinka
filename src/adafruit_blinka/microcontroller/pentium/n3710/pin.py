# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pentium N3710 (Braswell core SOC) pin names
   i2c and GPIO can be accessed through Blinka.
   For i2c use IC20_SCL, IC20-SDA and IC21-SCL, IC21-SDA in the i2c(<sdl, sda>) calls.
   For UART use pyserial"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# gpiochip3
GPIO_243 = Pin((3, 15))
GPIO_246 = Pin((3, 18))
GPIO_247 = Pin((3, 19))
GPIO_249 = Pin((3, 21))
GPIO_250 = Pin((3, 22))
GPIO_253 = Pin((3, 25))
GPIO_273 = Pin((3, 45))
GPIO_275 = Pin((3, 47))
GPIO_276 = Pin((3, 48))
GPIO_278 = Pin((3, 50))
GPIO_279 = Pin((3, 51))
GPIO_280 = Pin((3, 52))
GPIO_307 = Pin((3, 79))

SDIO_D3 = SDMMC2_D3 = GPIO_243
SDIO_DI = SDMMC2_D1 = GPIO_246
SDIO_CLK = SDMMC2_CLK = GPIO_247
SDIO_D2 = SDMMC2_D2 = GPIO_249
SDIO_CMD = SDMMC2_CMD = GPIO_250
SDIO_D0 = SDMMC2_D0 = GPIO_253

MF_LPC_AD2 = GPIO_273
MF_LPC_AD0 = GPIO_275
LPC_FRAMEB = GPIO_276
MF_LPC_AD3 = GPIO_278
MF_LPC_CLKOUT0 = GPIO_279
MF_LPC_AD1 = GPIO_280
ILB_SERIRQ = GPIO_307

# ggpiochip1
GPIO_358 = Pin((1, 17))
GPIO_SUS3 = SDIO_WAKE = GPIO_358


# gpiochip0
GPIO_490 = Pin((0, 76))
GPIO_492 = Pin((0, 78))

SATA_GP1 = TS_INT = GPIO_490
SATA_GP2 = TS_RST = GPIO_492


# not general gpio on chip 0
# use pyserial not blinka.  These are only included for completeness

UART1_RXD = Pin((0, 16))
UART1_TXD = Pin((0, 20))
UART1_RTS = Pin((0, 15))
UART1_CTS = Pin((0, 18))

UART2_RXD = Pin((0, 17))
UART2_TXD = Pin((0, 21))
UART2_RTS = Pin((0, 19))
UART2_CTS = Pin((0, 22))

GPIO_429 = UART1_RTS
GPIO_430 = UART1_RXD
GPIO_431 = UART2_RXD
GPIO_432 = UART1_CTS
GPIO_434 = UART1_TXD
GPIO_435 = UART2_TXD
GPIO_436 = UART2_CTS

# i2c use these addresses when accessing i2c from Blinka.  You can also access
# the i2c useing smbus
I2C0_SDA = Pin((0, 61))  # IC21 on diagram, port 0 in hardware manual
I2C0_SCL = Pin((0, 65))

I2C1_SDA = TS_I2C_SDA = Pin((0, 45))  # I2C2 on diagram, port 5 in hardware manual
I2C1_SCL = TS_I2C_SCL = Pin((0, 48))


GPIO_469 = I2C1_SDA  # I2C2 on diagram
GPIO_472 = I2C1_SCL
GPIO_475 = I2C0_SDA  # I2C1 on diagram
GPIO_479 = I2C0_SCL

# ordered as i2cId, sclId, sdaId
i2cPorts = ((0, I2C0_SCL, I2C0_SDA), (1, I2C1_SCL, I2C1_SDA))
