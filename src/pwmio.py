"""
`pwmio` - Support for PWM based protocols
===========================================================
See `CircuitPython:pwmio` in CircuitPython for more details.
Not supported by all boards.

* Author(s): Melissa LeBlanc-Williams
"""

import sys

from adafruit_blinka.agnostic import detector

# pylint: disable=unused-import

if detector.board.any_raspberry_pi:
    from adafruit_blinka.microcontroller.bcm283x.pulseio.PWMOut import PWMOut
elif detector.board.any_coral_board:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
elif detector.board.any_giant_board:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
elif detector.board.any_beaglebone:
    from adafruit_blinka.microcontroller.am335x.sysfs_pwmout import PWMOut
elif detector.board.any_rock_pi_board:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
elif detector.board.binho_nova:
    from adafruit_blinka.microcontroller.nova.pwmout import PWMOut
elif detector.board.greatfet_one:
    from adafruit_blinka.microcontroller.nxp_lpc4330.pwmout import PWMOut
elif detector.board.any_lubancat:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
elif "sphinx" in sys.modules:
    pass
else:
    raise NotImplementedError("pwmio not supported for this board.")
