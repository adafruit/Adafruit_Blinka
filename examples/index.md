This repository is structured around integration tests rooted at the `test/src`
directory, intended to test the compatibility layer rooted in `src`. 

The tests offer a procedural way to assert equivalence between 'native' CircuitPython behaviour and behaviour of the **adafruit_blinka** compatibility layer.

The structure of the testing modules permits test suites to be imported and configured selectively on different implementations, platforms and boards (see `adafruit_blinka.agnostic.py` for definitions of these terms).

Automated introspection of the python runtime combines with interactive prompts
to configure a scenario for testing (e.g. which platform, which board, what is wired to it)
so the same routines can be carried out on Micropython boards, dual boards running either CircuitPython or Micropython, or dedicated CircuitPython boards.

Typically the tests have first run on a native CircuitPython platform, and are then used to 
prove equivalence on a Micropython platform running the **adafruit_blinka** compatibility layer.

Tests of compatible versions of **digitalio**, **board** and **microcontroller** have successfully demonstrated
the same code running on either platform, setting and getting pin values and using pull.

Tests have also proven compatibility of the following unmodified CircuitPython libraries...

* adafruit_bme280
* adafruit_mma8451
* adafruit_gps

...which proves the fundamentals of bitbangio.I2C, busio.I2C and busio.UART

# Example

To take a minimal example, the following should assert the default behaviour of the DigitalInOut 
constructor, checks the behaviour of switch_to_input/output(), configures a pin as a pull-up button, a pull-down button and an LED.

```python
from testing import test_module_name
test_module_name("testing.universal.digitalio")
```

## Comments

There are reference routines in `test/scripts` like `upload_feather_huzzah_micropython_put.sh` which execute a selective bytecode-compile to .mpy format and an ampy upload for CircuitPython/Micropython on esp8266, or `upload_pyboard_micropython_cp.sh` which selectively bytecode-compiles and synchronizes files with cp to the CIRCUITPY or PYBFLASH disk mount for stm32 and samd21 platforms.