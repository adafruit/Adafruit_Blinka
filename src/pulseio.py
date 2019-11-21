from adafruit_blinka.agnostic import detector

if detector.board.any_raspberry_pi:
    from adafruit_blinka.microcontroller.bcm283x.pulseio.PulseIn import PulseIn
if detector.board.any_coral_board:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
if detector.board.any_giant_board:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
if detector.board.any_beaglebone:
    from adafruit_blinka.microcontroller.am335x.sysfs_pwmout import PWMOut
if detector.board.binho_nova:
    from adafruit_blinka.microcontroller.nova.pwmout import PWMOut
