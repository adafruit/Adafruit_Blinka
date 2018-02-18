"""
    Tests which require an embedded platform (with actual hardware bindings)
    but which are not architecture-specific.
"""
import unittest
import digitalio
from testing.board import default_pin

class TestDigitalInOut(unittest.TestCase):


    def test_context_manager(self):
        """Deinitialisation is triggered by __exit__()"""
        dio = digitalio.DigitalInOut(default_pin)
        self.assertIsNotNone(dio._pin)
        with dio:
            pass
        self.assertIsNone(dio._pin)

def main():
    unittest.main()
