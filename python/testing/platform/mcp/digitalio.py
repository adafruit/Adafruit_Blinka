"""
    Tests which require an embedded platform (with actual hardware bindings)
    but which are not architecture-specific.
"""
import unittest
import agnostic
import board

if agnostic.board == "feather_m0_express":
    LEDPIN = board.D13
else:
    raise NameError("No LED for {}".format(agnostic.platform))

class TestDigitalInOut(unittest.TestCase):


    def test_context_manager(self):
        """Deinitialisation is triggered by __exit__()"""
        dio = create_pin()
        self.assertIsNotNone(dio._pin)
        with dio:
            pass
        self.assertIsNone(dio._pin)

def main():
    unittest.main()
