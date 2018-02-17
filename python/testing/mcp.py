import unittest


class TestEnum(unittest.TestCase):
    """
        Verifies the repl() and str() behaviour of an example Enum
        Enums represent configuration values such as digitalio.Direction, digitalio.Pull etc.
    """

    def setUp(self):
        import mcp
        class Cls(mcp.Enum):
            pass
        Cls.one = Cls()
        Cls.two = Cls()
        # class refs would be implicitly populated correctly in a real module
        Cls.__module__ = "ho.hum"
        Cls.__qualname__ = "Example"
        self.Cls = Cls


    def test_iteritems(self):
        items = list(self.Cls.iteritems())
        self.assertEqual( items, [("one",self.Cls.one),("two",self.Cls.two),])


    def test_repr(self):
        name = "one"
        actual = repr(getattr(self.Cls, name))
        expected = "{}.{}.{}".format(self.Cls.__module__, self.Cls.__qualname__, name)
        self.assertEqual( actual, expected)


    def test_str(self):
        self.assertEqual(str(self.Cls.one), repr(self.Cls.one))