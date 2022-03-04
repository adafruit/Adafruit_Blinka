# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import unittest


class TestEnum(unittest.TestCase):
    """
    Verifies the repl() and str() behaviour of an example Enum
    Enums represent configuration values such as digitalio.Direction, digitalio.Pull etc.
    """

    def setUp(self):
        """Create an example Enum, mocking __module__ and __qualname__"""
        import adafruit_blinka

        class Cls(adafruit_blinka.Enum):
            pass

        Cls.one = Cls()
        Cls.two = Cls()
        # class refs would be implicitly populated correctly in a real module
        Cls.__module__ = "ho.hum"
        Cls.__qualname__ = "Example"
        self.Cls = Cls

    def test_iteritems(self):
        """A subtype of Enum can list all attributes of its own type"""
        items = list(self.Cls.iteritems())
        self.assertEqual(
            items,
            [
                ("one", self.Cls.one),
                ("two", self.Cls.two),
            ],
        )

    def test_repr(self):
        """A repr() call on an Enum gives its fully-qualified name"""
        name = "one"
        actual = repr(getattr(self.Cls, name))
        expected = "{}.{}.{}".format(self.Cls.__module__, self.Cls.__qualname__, name)
        self.assertEqual(actual, expected)

    def test_str(self):
        """A str() call on an Enum performs the same as repr()"""
        self.assertEqual(str(self.Cls.one), repr(self.Cls.one))


class TestDigitalInOut(unittest.TestCase):
    def test_context_manager(self):
        import digitalio
        from testing.board import default_pin

        """Deinitialisation is triggered by __exit__() and should dispose machine.pin reference"""
        dio = digitalio.DigitalInOut(default_pin)
        self.assertIsNotNone(dio._pin)
        with dio:
            pass
        self.assertIsNone(dio._pin)
