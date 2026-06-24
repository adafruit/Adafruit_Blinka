# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""TI AM625X pin names (BeaglePlay)"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# gpiochip1 (4201000.gpio) – MCU domain GPIO
QWIIC_SCL = Pin((1, 17))  # MCU_I2C0_SCL
QWIIC_SDA = Pin((1, 18))  # MCU_I2C0_SDA

# gpiochip2 (600000.gpio) – main_gpio0
USR0 = Pin((2, 3))   # USR0 LED
USR1 = Pin((2, 4))   # USR1 LED
USR2 = Pin((2, 5))   # USR2 LED
USR3 = Pin((2, 6))   # USR3 LED
USR4 = Pin((2, 9))   # USR4 LED
USR_BUTTON = Pin((2, 18))

# gpiochip3 (601000.gpio) – main_gpio1
# MIKROBUS I2C (i2c-3)
MIKROBUS_SCL = Pin((3, 22))  # MIKROBUS_GPIO1_22 / main_i2c3_scl
MIKROBUS_SDA = Pin((3, 23))  # MIKROBUS_GPIO1_23 / main_i2c3_sda

# Grove I2C (i2c-1)
GROVE_SCL = Pin((3, 28))  # main_i2c1_scl
GROVE_SDA = Pin((3, 29))  # main_i2c1_sda

# MIKROBUS general-purpose GPIO lines
MIKROBUS_GPIO1_7 = Pin((3, 7))
MIKROBUS_GPIO1_8 = Pin((3, 8))
MIKROBUS_GPIO1_9 = Pin((3, 9))
MIKROBUS_GPIO1_10 = Pin((3, 10))
MIKROBUS_GPIO1_11 = Pin((3, 11))
MIKROBUS_GPIO1_12 = Pin((3, 12))
MIKROBUS_W1 = Pin((3, 13))      # 1-Wire GPIO
MIKROBUS_GPIO1_14 = Pin((3, 14))
MIKROBUS_GPIO1_24 = Pin((3, 24))
MIKROBUS_GPIO1_25 = Pin((3, 25))

# ordered as (i2cId, SCL, SDA)
i2cPorts = (
    (3, MIKROBUS_SCL, MIKROBUS_SDA),  # MIKROBUS I2C → /dev/play/mikrobus/i2c
    (1, GROVE_SCL, GROVE_SDA),         # Grove I2C    → /dev/play/grove/i2c
    (5, QWIIC_SCL, QWIIC_SDA),         # QWIIC        → /dev/play/qwiic/i2c
)

# ordered as (spiId, sckId, mosiId, misoId)
# MIKROBUS SPI is managed by the Greybus/CC1352P7 coprocessor;
# no spidev is exposed by default on stock images.
spiPorts = ()

# ordered as (uartId, txId, rxId)
# MIKROBUS UART = /dev/ttyS0 (main_uart0)
uartPorts = ()
