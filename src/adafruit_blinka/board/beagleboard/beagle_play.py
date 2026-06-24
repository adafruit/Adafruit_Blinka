# SPDX-FileCopyrightText: 2026 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the BeaglePlay."""
from adafruit_blinka.microcontroller.ti.am625x import pin

# MIKROBUS connector I2C (i2c-3, /dev/play/mikrobus/i2c)
SCL = pin.MIKROBUS_SCL
SDA = pin.MIKROBUS_SDA

# QWIIC / STEMMA QT connector (i2c-5, /dev/play/qwiic/i2c)
QWIIC_SCL = pin.QWIIC_SCL
QWIIC_SDA = pin.QWIIC_SDA

# Grove connector I2C (i2c-1, /dev/play/grove/i2c)
GROVE_SCL = pin.GROVE_SCL
GROVE_SDA = pin.GROVE_SDA

# MIKROBUS general-purpose GPIO
MIKROBUS_GPIO1_7 = pin.MIKROBUS_GPIO1_7
MIKROBUS_GPIO1_8 = pin.MIKROBUS_GPIO1_8
MIKROBUS_GPIO1_9 = pin.MIKROBUS_GPIO1_9
MIKROBUS_GPIO1_10 = pin.MIKROBUS_GPIO1_10
MIKROBUS_GPIO1_11 = pin.MIKROBUS_GPIO1_11
MIKROBUS_GPIO1_12 = pin.MIKROBUS_GPIO1_12
MIKROBUS_W1 = pin.MIKROBUS_W1
MIKROBUS_GPIO1_14 = pin.MIKROBUS_GPIO1_14
MIKROBUS_GPIO1_24 = pin.MIKROBUS_GPIO1_24
MIKROBUS_GPIO1_25 = pin.MIKROBUS_GPIO1_25

# User LEDs (gpiochip2)
LED_USR0 = pin.USR0
LED_USR1 = pin.USR1
LED_USR2 = pin.USR2
LED_USR3 = pin.USR3
LED_USR4 = pin.USR4

# User button
USR_BUTTON = pin.USR_BUTTON
