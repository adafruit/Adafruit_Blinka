import sys
from adafruit_blinka.agnostic import board_id


if board_id == "raspi_2" or board_id == "raspi_3":
    from adafruit_blinka.microcontroller.raspi_23.pulseio.PulseIn import PulseIn as PulseIn

"""
class PulseIn:
    def __init__(self, pin, maxlen=2, idle_state=False):
        self.pulsein = _PulseIn.PulseIn(pin, maxlen, idle_state=idle_state)

    def deinit(self):
        self.pulsein.deinit()
    def pause(self):
        self.pulsein.pause()
    
    def resume(self, trigger_duration=0):
        self.pulsein(trigger_duration)
"""
