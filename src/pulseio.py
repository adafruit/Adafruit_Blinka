"""
`pulseio` - Pulse Width Modulation Input and Output control
=================================================
See `CircuitPython:pulseio` in CircuitPython for more details.
* Author(s): Melissa LeBlanc-Williams
"""

from adafruit_blinka.agnostic import detector

# pylint: disable=unused-import

if detector.board.any_raspberry_pi:
    from adafruit_blinka.microcontroller.bcm283x.pulseio.PulseIn import PulseIn
    from adafruit_blinka.microcontroller.bcm283x.pulseio.PWMOut import PWMOut
if detector.board.any_coral_board:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
if detector.board.any_giant_board:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
if detector.board.any_beaglebone:
    from adafruit_blinka.microcontroller.am335x.sysfs_pwmout import PWMOut
if detector.board.any_rock_pi_board:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
if detector.board.binho_nova:
    from adafruit_blinka.microcontroller.nova.pwmout import PWMOut
if detector.board.greatfet_one:
    from adafruit_blinka.microcontroller.nxp_lpc4330.pwmout import PWMOut
