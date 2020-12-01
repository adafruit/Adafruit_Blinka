"""NXP LPC4330 pin names"""
try:
    from greatfet import GreatFET
    from greatfet.interfaces.adc import ADC

    gf = GreatFET()
except ModuleNotFoundError:
    raise RuntimeError(
        "Unable to create GreatFET object. Make sure library is "
        "installed and the device is connected."
    ) from ModuleNotFoundError


class Pin:
    """A basic Pin class for the NXP LPC4330 that
    acts as a wrapper for the GreatFET api.
    """

    # pin modes
    OUT = gf.gpio.DIRECTION_OUT
    IN = gf.gpio.DIRECTION_IN
    ADC = 2
    DAC = 3

    # pin values
    LOW = 0
    HIGH = 1

    def __init__(self, pin_id=None):
        self.id = pin_id
        self._mode = None
        self._pin = None

    def init(self, mode=IN, pull=None):
        """Initialize the Pin"""
        if self.id is None:
            raise RuntimeError("Can not init a None type pin.")
        if pull is not None:
            raise NotImplementedError("Internal pullups and pulldowns not supported")
        if mode in (Pin.IN, Pin.OUT):
            if self.id not in gf.GPIO_MAPPINGS:
                raise ValueError("Pin does not have GPIO capabilities")
            self._pin = gf.gpio.get_pin(self.id)
            self._pin.set_direction(mode)
        elif mode == Pin.ADC:
            # ADC only available on these pins
            if self.id not in gf.ADC_MAPPINGS:
                raise ValueError("Pin does not have ADC capabilities")
            self._pin = ADC(gf, self.id)
        elif mode == Pin.DAC:
            # DAC only available on these pins
            if self.id != "J2_P5":
                raise ValueError("Pin does not have DAC capabilities")
            self._pin = gf.apis.dac
            self._pin.initialize()
        else:
            raise ValueError("Incorrect pin mode: {}".format(mode))
        self._mode = mode

    def value(self, val=None):
        """Set or return the Pin Value"""
        # Digital In / Out
        if self._mode in (Pin.IN, Pin.OUT):
            # digital read
            if val is None:
                return self._pin.get_state()
            # digital write
            if val in (Pin.LOW, Pin.HIGH):
                self._pin.set_state(val)
                return None
            # nope
            raise ValueError("Invalid value for pin.")
        # Analog In
        if self._mode == Pin.ADC:
            if val is None:
                # Read ADC here
                return self._pin.read_samples()[0]
            # read only
            raise AttributeError("'AnalogIn' object has no attribute 'value'")
        # Analog Out
        if self._mode == Pin.DAC:
            if val is None:
                # write only
                raise AttributeError("unreadable attribute")
            # Set DAC Here
            self._pin.set_value(int(val))
            return None
        raise RuntimeError(
            "No action for mode {} with value {}".format(self._mode, val)
        )


# create pin instances for each pin
# J1 Header Pins
J1_P3 = Pin("J1_P3")
J1_P4 = Pin("J1_P4")
J1_P5 = Pin("J1_P5")
J1_P6 = Pin("J1_P6")
J1_P7 = Pin("J1_P7")
J1_P8 = Pin("J1_P8")
J1_P9 = Pin("J1_P9")
J1_P10 = Pin("J1_P10")
J1_P12 = Pin("J1_P12")
J1_P13 = Pin("J1_P13")
J1_P14 = Pin("J1_P14")
J1_P15 = Pin("J1_P15")
J1_P16 = Pin("J1_P16")
J1_P17 = Pin("J1_P17")
J1_P18 = Pin("J1_P18")
J1_P19 = Pin("J1_P19")
J1_P20 = Pin("J1_P20")
J1_P21 = Pin("J1_P21")
J1_P22 = Pin("J1_P22")
J1_P23 = Pin("J1_P23")
J1_P24 = Pin("J1_P24")
J1_P25 = Pin("J1_P25")
J1_P26 = Pin("J1_P26")
J1_P27 = Pin("J1_P27")
J1_P28 = Pin("J1_P28")
J1_P29 = Pin("J1_P29")
J1_P30 = Pin("J1_P30")
J1_P31 = Pin("J1_P31")
J1_P32 = Pin("J1_P32")
J1_P33 = Pin("J1_P33")
J1_P34 = Pin("J1_P34")
J1_P35 = Pin("J1_P35")
J1_P37 = Pin("J1_P37")
J1_P39 = Pin("J1_P39")  # MOSI
J1_P40 = Pin("J1_P40")  # MISO


# J2 Header Pins
J2_P3 = Pin("J2_P3")
J2_P4 = Pin("J2_P4")
J2_P5 = Pin("J2_P5")  # ADC, ADC, DAC
J2_P6 = Pin("J2_P6")
J2_P7 = Pin("J2_P7")
J2_P8 = Pin("J2_P8")
J2_P9 = Pin("J2_P9")  # ADC, GPIO
J2_P10 = Pin("J2_P10")
J2_P13 = Pin("J2_P13")
J2_P14 = Pin("J2_P14")
J2_P15 = Pin("J2_P15")
J2_P16 = Pin("J2_P16")  # GPIO, ADC
J2_P18 = Pin("J2_P18")
J2_P19 = Pin("J2_P19")
J2_P20 = Pin("J2_P20")
J2_P22 = Pin("J2_P22")
J2_P23 = Pin("J2_P23")
J2_P24 = Pin("J2_P24")
J2_P25 = Pin("J2_P25")
J2_P27 = Pin("J2_P27")
J2_P28 = Pin("J2_P28")
J2_P29 = Pin("J2_P29")
J2_P30 = Pin("J2_P30")
J2_P31 = Pin("J2_P31")
J2_P33 = Pin("J2_P33")
J2_P34 = Pin("J2_P34")
J2_P35 = Pin("J2_P35")
J2_P36 = Pin("J2_P36")
J2_P37 = Pin("J2_P37")
J2_P38 = Pin("J2_P38")

# Bonus Row Pins
J7_P2 = Pin("J7_P2")
J7_P3 = Pin("J7_P3")
J7_P4 = Pin("J7_P4")  # ADC, ADC
J7_P5 = Pin("J7_P5")  # ADC, ADC
J7_P6 = Pin("J7_P6")
J7_P7 = Pin("J7_P7")
J7_P8 = Pin("J7_P8")
J7_P13 = Pin("J7_P13")
J7_P14 = Pin("J7_P14")
J7_P15 = Pin("J7_P15")
J7_P16 = Pin("J7_P16")
J7_P17 = Pin("J7_P17")
J7_P18 = Pin("J7_P18")

SCL = Pin()
SDA = Pin()

SCK = Pin()
MOSI = J1_P39
MISO = J1_P40

TX = J1_P33
RX = J1_P34

# ordered as uartId, txId, rxId
uartPorts = ((0, TX, RX),)

# pwm outputs: pwm channel and pin
pwmOuts = (
    (0, J1_P4),
    (1, J1_P6),
    (2, J1_P28),
    (3, J1_P30),
    (4, J2_P36),
    (5, J2_P34),
    (6, J2_P33),
    (7, J1_P34),
    (8, J2_P9),
    (9, J1_P6),
    (10, J1_P25),
    (11, J1_P32),
    (12, J1_P31),
    (13, J2_P3),
    (14, J1_P3),
    (15, J1_P5),
)
