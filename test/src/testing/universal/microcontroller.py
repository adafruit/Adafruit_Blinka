import unittest

class TestMicrocontrollerModule(unittest.TestCase):

    def test_pins_exist(self):
        """The microcontroller module should contain pin references"""
        import microcontroller
        from microcontroller import pin
        from testing.microcontroller import pin_count
        entries = [getattr(pin, key) for key in dir(pin)]
        # is this filter line needed? any other types valid in pin module?
        entries = list(filter(lambda val: type(val) is microcontroller.Pin, entries))
        self.assertTrue(len(entries) > 0)
        self.assertTrue(len(entries) == pin_count)