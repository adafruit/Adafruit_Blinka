import unittest
import agnostic


class TestMicrocontrollerModule(unittest.TestCase):


    def test_pins_exist(self):
        import microcontroller
        import microcontroller.pin as pin
        entries = [getattr(pin, key) for key in dir(pin)]
        # is this filter line needed? any other types valid in pin module?
        entries = list(filter(lambda val: type(val) is microcontroller.Pin, entries))
        if agnostic.platform == "esp8266":
            self.assertTrue(len(entries) == 10)