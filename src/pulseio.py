from adafruit_blinka.agnostic import detector

if detector.board.any_raspberry_pi:
    from adafruit_blinka.microcontroller.bcm283x.pulseio.PulseIn import PulseIn
