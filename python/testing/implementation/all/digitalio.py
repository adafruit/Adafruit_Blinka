import unittest
from testing import yes_no
from testing.board import led_pin,default_pin

class TestDigitalInOut(unittest.TestCase):


    def test_default(self):
        import digitalio
        """Check that a DigitalInOut is input with no pull when constructed"""
        with digitalio.DigitalInOut(default_pin) as dio:
            self.assertEqual(dio.direction, digitalio.Direction.INPUT)
            self.assertEqual(dio.pull, None)


    def test_blink(self):
        import digitalio
        from agnostic import time
        self.assertTrue(yes_no("Is LED wired to {}".format(led_pin)))
        with digitalio.DigitalInOut(led_pin) as led:
            led.direction = digitalio.Direction.OUTPUT
            # should now be OUT, PUSH_PULL, value=0, and LED should light
            self.assertTrue(yes_no("Is LED lit"))
            for count in range(3):
                led.value = True
                time.sleep(1.0)
                led.value = False
                time.sleep(1.0)
            self.assertTrue(yes_no("Did LED wink thrice"))
