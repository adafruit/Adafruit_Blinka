This repository is structured around integration tests found in the python/testing
directory. The tests offer a procedural way to assert equivalence between 'native' CircuitPython (CP) behaviour and 
behaviour of the MicropythonCircuitPython (MCP) layer.


In particular, automated introspection of the python runtime combines with interactive prompts
to configure a scenario for testing (e.g. which platform, which board, what is wired to it) meaning that 
the same routines can be carried out on Micropython boards, dual boards running either CP or MCP
or dedicated CP boards. 

From a project-management point of view, tests can provide a strictly-interpreted way to 
communicate missing features, also providing the implicit means of verifying that intended 
features for the MCP layer are in fact already served from the CP layer.

# Example

To take a minimal example, the following asserts the default behaviour of the DigitalInOut 
constructor, checks the behaviour of switch_to_input/output(), configures a pin as a pull-up button, a pull-down button and an LED.

```python
import testing
testing.main()
```

## Comments

There are routines in the top level of the repo like `upload_feather_m0_watch.py` which selectively synchronize files it with the CIRCUITPY or PYBFLASH folder for stm32 and samd21 (with a file-watching behaviour for edits), or which execute a selective ampy upload for CircuitPython/Micropython on esp8266.

Given the limited memory available, on the Feather M0 Express, running the test case requires that 
the [micropython-lib unittest library](https://github.com/micropython/micropython-lib/blob/master/unittest/unittest.py) 
is distributed as a compatible Micropython bytecode .mpy file 
pre-compiled under an mpy-cross version from the CircuitPython 2.2.3-tagged repository. Otherwise
simply loading the unittest module already busts the available memory. 

# Test Suite Structure

The structure of the testing modules is as follows, to permit test suites to be imported selectively
on different implementations, platforms and boards (see agnostic.py for definitions of these terms)...

* _testing_ - common function definitions for suite-execution
* _testing.mcp_ - test suite for hardware-agnostic elements of MCP layer (e.g. Enum)
* _testing.implementation_ - calculates implementation-specific parameters for test fixtures
* _testing.implementation.all_ - suites expected to run on all platforms
* _testing.implementation.micropython_ - suites testing MCP-specific classes and behaviours (under the hood of the hardware compatibility layer) and only 
expected to run on Micropython
* _testing.implementation.circuitpython - suites testing CircuitPython-specific 
classes and behaviours, and only expected to run in CircuitPython_

e.g.
* testing.implementation.all.digitalio - tests against the 
digitalio module regardless of platform
* testing.implementation.circuitpython.digitalio - tests of digitalio against a 
native circuitpython host
* testing.implementation.micropython.digitalio - tests of digitalio against the MCP
compatibility layer


# Next Steps 

To be able to run a substantial series of testing modules, a dedicated 
feather m0 express firmware image should be prepared with [frozen modules](https://learn.adafruit.com/micropython-for-samd21/frozen-modules) which 
minimises overhead by holding test definitions in flash instead of RAM.
