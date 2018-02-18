import unittest
from testing.platform import led_pin,default_pin

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
        with digitalio.DigitalInOut(led_pin) as led:
            led.direction = digitalio.Direction.OUTPUT
            result = input("LED wired to {} (Y/n)?".format(led))
            if result.lower() != 'n':
                led.value = True
                time.sleep(0.1)
                led.value = False
                time.sleep(0.1)
                result = input("Blinked (Y/n)?")
                self.assertTrue(result.lower() != 'n')
