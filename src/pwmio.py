# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
`pwmio` - Support for PWM based protocols
===========================================================
See `CircuitPython:pwmio` in CircuitPython for more details.
Not supported by all boards.

* Author(s): Melissa LeBlanc-Williams
"""
# pylint: disable=too-many-boolean-expressions
import sys

from adafruit_blinka.agnostic import detector

# pylint: disable=unused-import

if detector.board.any_raspberry_pi and not detector.board.RASPBERRY_PI_5:
    from adafruit_blinka.microcontroller.bcm283x.pwmio.PWMOut import PWMOut
elif detector.board.any_coral_board:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
elif detector.board.any_giant_board:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
elif detector.board.any_pcduino_board:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
elif detector.board.any_beaglebone:
    from adafruit_blinka.microcontroller.am335x.sysfs_pwmout import PWMOut
elif detector.board.any_lemaker:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
elif detector.board.any_siemens_simatic_iot2000:
    from adafruit_blinka.microcontroller.am65xx.pwmout import PWMOut
elif detector.board.any_odroid_40_pin:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
elif detector.board.any_rock_pi_board:
    from adafruit_blinka.microcontroller.rockchip.PWMOut import PWMOut
elif detector.board.binho_nova:
    from adafruit_blinka.microcontroller.nova.pwmout import PWMOut
elif detector.board.greatfet_one:
    from adafruit_blinka.microcontroller.nxp_lpc4330.pwmout import PWMOut
elif detector.board.any_lubancat:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
elif detector.board.pico_u2if:
    from adafruit_blinka.microcontroller.rp2040_u2if.pwmio import PWMOut
elif (
    detector.board.feather_u2if
    or detector.board.feather_can_u2if
    or detector.board.feather_epd_u2if
    or detector.board.feather_rfm_u2if
    or detector.board.qtpy_u2if
    or detector.board.itsybitsy_u2if
    or detector.board.macropad_u2if
    or detector.board.qt2040_trinkey_u2if
    or detector.board.kb2040_u2if
):
    from adafruit_blinka.microcontroller.rp2040_u2if.pwmio import PWMOut
elif "sphinx" in sys.modules:
    pass
else:
    raise NotImplementedError("pwmio not supported for this board.")
