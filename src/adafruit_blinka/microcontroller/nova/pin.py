class Pin:
    """A basic Pin class for use with Binho Nova."""

    IN = 'DIN'
    OUT = 'DOUT'
    AIN = 'AIN'
    AOUT = 'AOUT'
    PWM = 'PWM'
    LOW = 0
    HIGH = 1

    _nova = None

    def __init__(self, pin_id=None):
        if not Pin._nova:
            from binhoHostAdapter import binhoHostAdapter
            from binhoHostAdapter import binhoUtilities

            utilities = binhoUtilities.binhoUtilities()
            devices = utilities.listAvailableDevices()

            if len(devices) > 0:
                Pin._nova = binhoHostAdapter.binhoHostAdapter(devices[0])
        # check if pin is valid
        if pin_id > 4:
            raise ValueError("Invalid pin {}.".format(pin_id))

        self.id = pin_id

    def init(self, mode=IN, pull=None):
        if self.id is None:
            raise RuntimeError("Can not init a None type pin.")
        # Nova does't have configurable internal pulls for 
        if pull:
            raise ValueError("Internal pull up/down not currently supported.")
        Pin._nova.setIOpinMode(self.id, mode)

    def value(self, val=None):
        if self.id is None:
            raise RuntimeError("Can not access a None type pin.")
        # read
        if val is None:
            return int(Pin._nova.getIOpinValue(self.id).split('VALUE ')[1])
        # write
        elif val in (self.LOW, self.HIGH):
            Pin._nova.setIOpinValue(self.id, val)
        else:
            raise RuntimeError("Invalid value for pin")

# create pin instances for each pin
IO0 = Pin(0)
IO1 = Pin(1)
IO2 = Pin(2)
IO3 = Pin(3)
IO4 = Pin(4)

PWM0 = IO0
PWM1 = IO1
PWM2 = IO2
# No PWM support on IO3
PWM4 = IO4

pwmOuts = ( ((1, 0), PWM0), ((1, 1), PWM1), ((1, 2), PWM2), ((1, 4), PWM4) )