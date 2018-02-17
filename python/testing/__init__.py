import unittest

def test_module(m, runner=None):
    if runner is None:
        runner = unittest.TestRunner()
    suite = unittest.TestSuite()
    for key in dir(m):
        val = getattr(m, key)
        try:
            if issubclass(val, unittest.TestCase):
                suite.addTest(val)
        except:
            pass
    return runner.run(suite)