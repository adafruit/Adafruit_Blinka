# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the Beaglebone Blue."""
from adafruit_blinka.microcontroller.am335x import pin

# common to all beagles
LED_USR0 = pin.USR0
LED_USR1 = pin.USR1
LED_USR2 = pin.USR2
LED_USR3 = pin.USR3


# Reference: https://git.beagleboard.org/beagleboard/beaglebone-blue/-/blob/master/BeagleBone_Blue_Pin_Table.csv
SDA = pin.P8_17  # I2C1_SDA
SCL = pin.P8_18  # I2C1_SCL
