"""Tests which should run on Micropython or CPython regardless of platform"""
from testing import test_module
import testing.mcp
import testing.microcontroller

def main():
    test_module(testing.mcp)
    test_module(testing.microcontroller)

if __name__ == "__main__":
    main()