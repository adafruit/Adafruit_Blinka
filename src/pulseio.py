from adafruit_blinka.agnostic import detector

if detector.board.any_raspberry_pi_2_or_3:
    from adafruit_blinka.microcontroller.bcm283x.pulseio.PulseIn import PulseIn
