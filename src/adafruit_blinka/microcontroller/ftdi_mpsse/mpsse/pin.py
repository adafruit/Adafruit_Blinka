"""MPSSE pin names"""

from adafruit_blinka.microcontroller.ftdi_mpsse.mpsse.url import (
    get_ft232h_url,
    get_ft2232h_url,
)


class Pin:
    """A basic Pin class for use with FTDI MPSSEs."""

    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2

    mpsse_gpio = None

    def __init__(self, pin_id=None, interface_id=None):
        # setup GPIO controller if not done yet
        # use one provided by I2C as default
        if not Pin.mpsse_gpio:
            # pylint: disable=import-outside-toplevel
            from pyftdi.i2c import I2cController

            # pylint: enable=import-outside-toplevel

            i2c = I2cController()
            if interface_id is None:
                i2c.configure(get_ft232h_url())
            else:
                i2c.configure(get_ft2232h_url(interface_id))
            Pin.mpsse_gpio = i2c.get_gpio()
        # check if pin is valid
        if pin_id:
            if Pin.mpsse_gpio.all_pins & 1 << pin_id == 0:
                raise ValueError("Can not use pin {} as GPIO.".format(pin_id))
        # ID is just bit position
        self.id = pin_id

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        if not self.id:
            raise RuntimeError("Can not init a None type pin.")
        # MPSSE does't have configurable internal pulls?
        if pull:
            raise NotImplementedError("Internal pull up/down not currently supported.")
        pin_mask = Pin.mpsse_gpio.pins | 1 << self.id
        current = Pin.mpsse_gpio.direction
        if mode == self.OUT:
            current |= 1 << self.id
        else:
            current &= ~(1 << self.id)
        Pin.mpsse_gpio.set_direction(pin_mask, current)

    def value(self, val=None):
        """Set or return the Pin Value"""
        if not self.id:
            raise RuntimeError("Can not access a None type pin.")
        current = Pin.mpsse_gpio.read(with_output=True)
        # read
        if val is None:
            return 1 if current & 1 << self.id != 0 else 0
        # write
        if val in (self.LOW, self.HIGH):
            if val == self.HIGH:
                current |= 1 << self.id
            else:
                current &= ~(1 << self.id)
            # must mask out any input pins
            Pin.mpsse_gpio.write(current & Pin.mpsse_gpio.direction)
            return None
        # release the kraken
        raise RuntimeError("Invalid value for pin")
