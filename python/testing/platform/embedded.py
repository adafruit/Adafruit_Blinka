"""
    Tests which require an embedded platform (with actual hardware bindings)
    but which are not architecture-specific.
"""
import unittest
import agnostic
import board

if agnostic.platform == "esp8266":
    LEDPIN = board.D13
else:
    raise NameError("No LED for {}".format(agnostic.platform))

class TestDigitalInOut(unittest.TestCase):


    def test_default(self):
        """Check that a DigitalInOut is an input with constructed"""
        import digitalio
        from microcontroller import Pin
        pin = next(Pin.iteritems())  # grab any pin
        dio = digitalio.DigitalInOut(pin)
        self.assertEqual(dio.direction, digitalio.Direction.INPUT)
        self.assertEqual(dio.pull, digitalio.Pull.DOWN)


    def test_blink(self):
        import digitalio
        from utime import sleep
        led = digitalio.DigitalInOut(LEDPIN)
        led.direction = digitalio.Direction.OUTPUT
        while True:
            led.value = True
            sleep(0.1)
            led.value = False
            sleep(0.1)

def main():
    unittest.main()
