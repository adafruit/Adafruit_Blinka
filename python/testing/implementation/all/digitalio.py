import unittest
from testing import yes_no, await_true
from testing.board import led_pin, default_pin
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
        from agnostic import sleep
        self.assertTrue(yes_no("Is LED wired to {}".format(led_pin)))
        with digitalio.DigitalInOut(led_pin) as led:
            led.direction = digitalio.Direction.OUTPUT
            # should now be OUT, PUSH_PULL, value=0, and LED should light
            self.assertTrue(yes_no("Is LED lit"))
            for count in range(2):
                led.value = True
                sleep(0.5)
                led.value = False
                sleep(0.5)
            self.assertTrue(yes_no("Did LED wink twice"))

    def test_button_pull_up(self):
        """Pull-up button configured and detected"""
        if yes_no("Is Button wired to {} to GND".format(default_pin)):
            with digitalio.DigitalInOut(default_pin) as button:
                button.direction = digitalio.Direction.INPUT
                try:
                    button.pull = digitalio.Pull.UP
                except NotImplementedError as e:
                    print(e)
                    return
                self.assertTrue(button.value == 1)
                self.assertTrue(await_true("button pressed", lambda: button.value == 0))

    def test_button_pull_down(self):
        """Pull-down button configured and detected"""
        if(yes_no("Is Button wired from {} to VCC".format(default_pin))):
            with digitalio.DigitalInOut(default_pin) as button:
                button.direction = digitalio.Direction.INPUT
                try:
                    button.pull = digitalio.Pull.DOWN
                except NotImplementedError as e:
                    print(e)
                    return
                self.assertTrue(button.value == 0)
                self.assertTrue(await_true("button pressed", lambda: button.value == 1))

