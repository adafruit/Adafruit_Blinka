from adafruit_blinka.agnostic import detector

if detector.board.any_raspberry_pi:
    from adafruit_blinka.microcontroller.bcm283x.pulseio.PulseIn import PulseIn
if detector.board.any_coral_board:
    from adafruit_blinka.microcontroller.generic_linux.sysfs_pwmout import PWMOut
