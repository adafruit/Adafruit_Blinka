"""Tests which should run on Micropython or CPython regardless of platform"""
import unittest

def main():
#    suite = unittest.TestSuite()
#    suite.tests.append()
    unittest.main("testing.mcp")
    unittest.main("testing.microcontroller")

if __name__ == "__main__":
    main()