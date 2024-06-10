# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""CVITEK CV1800B pin names"""

# from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin
from adafruit_blinka.microcontroller.generic_linux.sysfs_pin import Pin

# see milkvduo/sdk_linux/duo-buildroot-sdk/buildroot-2021.05/
#   package/python-pinpong/pinpong/extension/milkvDuo.py
GP0 = Pin(508)
GP1 = Pin(509)
GP2 = Pin(378)
GP3 = Pin(377)
GP4 = Pin(371)
GP5 = Pin(372)
GP6 = Pin(375)
GP7 = Pin(374)
GP8 = Pin(373)
GP9 = Pin(370)
GP10 = Pin(425)
GP11 = Pin(426)
GP12 = Pin(496)
GP13 = Pin(497)
GP14 = Pin(494)
GP15 = Pin(495)
GP16 = Pin(503)
GP17 = Pin(504)
GP18 = Pin(502)
GP19 = Pin(505)
GP20 = Pin(507)
GP21 = Pin(506)
GP22 = Pin(356)
GP25 = Pin(440)
GP26 = Pin(451)
GP27 = Pin(454)

# SPI
SPI2_CS = GP9
SPI2_SCLK = GP6
SPI2_MISO = GP8
SPI2_MOSI = GP7

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SPI2_SCLK, SPI2_MOSI, SPI2_MISO),)
