import unittest
from testing import yes_no, await_true
from testing.board import led_pin, default_pin, led_hardwired, led_inverted
import digitalio
from digitalio import * # TODO refactor below for wildcard import


class TestDigitalInOut(unittest.TestCase):

    def test_default(self):
        """DigitalInOut is input with no pull when constructed"""
        with digitalio.DigitalInOut(default_pin) as dio:
            self.assertEqual(dio.direction, digitalio.Direction.INPUT)
            self.assertEqual(dio.pull, None)

    def test_switch_to_output(self):
        """Default configuration of switch_to_output is respected"""
        with digitalio.DigitalInOut(default_pin) as dio:
            dio.switch_to_output()
            self.assertEqual(dio.direction, digitalio.Direction.OUTPUT)
            self.assertEqual(dio.value, 0)
            self.assertEqual(dio.drive_mode, digitalio.DriveMode.PUSH_PULL)

    def test_switch_to_input(self):
        """Default configuration of switch_to_input is respected"""
        with digitalio.DigitalInOut(default_pin) as dio:
            dio.switch_to_output() # starts as input anyway
            dio.switch_to_input()
            self.assertEqual(dio.direction, digitalio.Direction.INPUT)
            self.assertEqual(dio.pull, None)


class TestDigitalInOutInteractive(unittest.TestCase):

    def test_blink(self):
        """LED blinks when proper attributes set"""
        print()
        from agnostic import sleep
        if not(led_hardwired) and not(yes_no("Is LED wired to {}".format(led_pin))):
            return # test trivially passed
        with digitalio.DigitalInOut(led_pin) as led:
            led.direction = digitalio.Direction.OUTPUT
            # should now be OUT, PUSH_PULL, value=0, and LED should light
            led.value = 0 if led_inverted else 1
            self.assertTrue(yes_no("Is LED lit"))
            print("Winking LED...")
            for count in range(2):
                led.value = not(led.value)
                sleep(0.5)
                led.value = not(led.value)
                sleep(0.5)
            self.assertTrue(yes_no("Did LED wink twice"))

    def test_button_pull_up(self):
        print()
        """Pull-up button configured and detected"""
        with digitalio.DigitalInOut(default_pin) as button:
            #button.direction = digitalio.Direction.INPUT # implied
            try:
                button.pull = digitalio.Pull.UP
            except NotImplementedError as e:
                print()
                print(e)
                return  # test trivially passed
            if yes_no("Is Button wired from {} to GND".format(default_pin)):
                self.assertTrue(button.value == 1)
                self.assertTrue(await_true("button pressed", lambda: button.value == 0))

    def test_button_pull_down(self):
        print()
        """Pull-down button configured and detected"""
        with digitalio.DigitalInOut(default_pin) as button:
            #button.direction = digitalio.Direction.INPUT # implied
            try:
                button.pull = digitalio.Pull.DOWN
            except NotImplementedError as e:
                print(e)
                return  # test trivially passed
            if (yes_no("Is Button wired from {} to VCC".format(default_pin))):
                self.assertTrue(button.value == 0)
                self.assertTrue(await_true("button pressed", lambda: button.value == 1))

