import Adafruit_BBIO.GPIO as GPIO

# Pins dont exist in CPython so...lets make our own!
class Pin:
    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1
    PULL_NONE = 0
    PULL_UP = 1
    PULL_DOWN = 2

    id = None
    _value = LOW
    _mode = IN

    def __init__(self, pin_name):
        self.id = pin_name

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other

    def init(self, mode=IN, pull=None):
        if mode != None:
            if mode == self.IN:
                self._mode = self.IN
                GPIO.setup(self.id, GPIO.IN)
            elif mode == self.OUT:
                self._mode = self.OUT
                GPIO.setup(self.id, GPIO.OUT)
            else:
                raise RuntimeError("Invalid mode for pin: %s" % self.id)
        if pull != None:
            if self._mode != self.IN:
                raise RuntimeError("Cannot set pull resistor on output")
            if pull == self.PULL_UP:
                GPIO.setup(self.id, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            elif pull == self.PULL_DOWN:
                GPIO.setup(self.id, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            else:
                raise RuntimeError("Invalid pull for pin: %s" % self.id)

    def value(self, val=None):
        if val != None:
            if val == self.LOW:
                self._value = val
                GPIO.output(self.id, val)
            elif val == self.HIGH:
                self._value = val
                GPIO.output(self.id, val)
            else:
                raise RuntimeError("Invalid value for pin")
        else:
            return GPIO.input(self.id)


# PocketBeagle
# P1_1 = SYS VIN
P1_2 = Pin('P1_2')  # GPIO_87
P1_3 = Pin('P1_3')  # GPIO_109
P1_4 = Pin('P1_4')  # GPIO_89
# P1_5 = USB VBUS
P1_6 = Pin('P1_6')  # GPIO_5
# P1_7 = USB VIN
P1_8 = Pin('P1_8')  # GPIO_2
# P1_9 = USB DN
P1_10 = Pin('P1_10')  # GPIO_3
# P1_11 = USB DP
P1_12 = Pin('P1_12')  # GPIO_4
# P1_13 = USB ID
# P1_14 = SYS 3.3V
# P1_15 = SYS GND
# P1_16 = SYS GND
# P1_17 = AIN 1.8V REF-
# P1_18 = AIN 1.8V REF+
P1_19 = Pin('P1_19')  # AIN0
P1_20 = Pin('P1_20')  # GPIO_20
P1_21 = Pin('P1_21')  # AIN1
# P1_22 = SYS GND
P1_23 = Pin('P1_23')  # AIN2
# P1_22 = SYS VOUT
P1_25 = Pin('P1_25')  # AIN3
P1_26 = Pin('P1_26')  # GPIO_12
P1_27 = Pin('P1_27')  # AIN4
P1_28 = Pin('P1_28')  # GPIO_13
P1_29 = Pin('P1_29')  # GPIO_117
P1_30 = Pin('P1_30')  # GPIO_43
P1_31 = Pin('P1_31')  # GPIO_114
P1_32 = Pin('P1_32')  # GPIO_42
P1_33 = Pin('P1_33')  # GPIO_111
P1_34 = Pin('P1_34')  # GPIO_26
P1_35 = Pin('P1_35')  # GPIO_88
P1_36 = Pin('P1_36')  # GPIO_110


P2_1 = Pin('P2_1')  # GPIO_50
P2_2 = Pin('P2_2')  # GPIO_59
P2_3 = Pin('P2_3')  # GPIO_23
P2_4 = Pin('P2_4')  # GPIO_58
P2_5 = Pin('P2_5')  # GPIO_30
P2_6 = Pin('P2_6')  # GPIO_57
P2_7 = Pin('P2_7')  # GPIO_31
P2_8 = Pin('P2_8')  # GPIO_60
P2_9 = Pin('P2_9')  # GPIO_15
P2_10 = Pin('P2_10')  # GPIO_52
P2_11 = Pin('P2_11')  # GPIO_14
# P2_12 = SYS  PWR BTN
# P2_13 = SYS VOUT
# P2_14 = BAT VIN
# P2_15 = SYS GND
# P2_16 = BAT TEMP
P2_17 = Pin('P2_17')  # GPIO_65
P2_18 = Pin('P2_18')  # GPIO_47
P2_19 = Pin('P2_19')  # GPIO_27
P2_20 = Pin('P2_20')  # GPIO_64
# P2_21 = SYS GND
P2_22 = Pin('P2_22')  # GPIO_46
# P2_23 = SYS 3.3V
P2_24 = Pin('P2_24')  # GPIO_44
P2_25 = Pin('P2_25')  # GPIO_41
# P2_26 = SYS NRST
P2_27 = Pin('P2_27')  # GPIO_40
P2_28 = Pin('P2_28')  # GPIO_116
P2_29 = Pin('P2_29')  # GPIO_7
P2_30 = Pin('P2_30')  # GPIO_113
P2_31 = Pin('P2_31')  # GPIO_19
P2_32 = Pin('P2_32')  # GPIO_112
P2_33 = Pin('P2_33')  # GPIO_45
P2_34 = Pin('P2_34')  # GPIO_115
P2_35 = Pin('P2_35')  # GPIO_86
P2_36 = Pin('P2_36')  # AIN7


# BeagleBone Black
# P8_1 = DGND
# P8_2 = DGND
P8_3 = Pin('P8_3')  # GPIO_38
P8_4 = Pin('P8_4')  # GPIO_39
P8_5 = Pin('P8_5')  # GPIO_34
P8_6 = Pin('P8_6')  # GPIO_35
P8_7 = Pin('P8_7')  # GPIO_66
P8_8 = Pin('P8_8')  # GPIO_67
P8_9 = Pin('P8_9')  # GPIO_69
P8_10 = Pin('P8_10')  # GPIO_68
P8_11 = Pin('P8_11')  # GPIO_45
P8_12 = Pin('P8_12')  # GPIO_44
P8_13 = Pin('P8_13')  # GPIO_23
P8_14 = Pin('P8_14')  # GPIO_26
P8_15 = Pin('P8_15')  # GPIO_47
P8_16 = Pin('P8_16')  # GPIO_46
P8_17 = Pin('P8_17')  # GPIO_27
P8_18 = Pin('P8_18')  # GPIO_65
P8_19 = Pin('P8_19')  # GPIO_22
P8_20 = Pin('P8_20')  # GPIO_63
P8_21 = Pin('P8_21')  # GPIO_62
P8_22 = Pin('P8_22')  # GPIO_37
P8_23 = Pin('P8_23')  # GPIO_36
P8_24 = Pin('P8_24')  # GPIO_33
P8_25 = Pin('P8_25')  # GPIO_32
P8_26 = Pin('P8_26')  # GPIO_61
P8_27 = Pin('P8_27')  # GPIO_86
P8_28 = Pin('P8_28')  # GPIO_88
P8_29 = Pin('P8_29')  # GPIO_87
P8_30 = Pin('P8_30')  # GPIO_89
P8_31 = Pin('P8_31')  # GPIO_10
P8_32 = Pin('P8_32')  # GPIO_11
P8_33 = Pin('P8_33')  # GPIO_9
P8_34 = Pin('P8_34')  # GPIO_81
P8_35 = Pin('P8_35')  # GPIO_8
P8_36 = Pin('P8_36')  # GPIO_80
P8_37 = Pin('P8_37')  # GPIO_78
P8_38 = Pin('P8_38')  # GPIO_79
P8_39 = Pin('P8_39')  # GPIO_76
P8_40 = Pin('P8_40')  # GPIO_77
P8_41 = Pin('P8_41')  # GPIO_74
P8_42 = Pin('P8_42')  # GPIO_75
P8_43 = Pin('P8_43')  # GPIO_72
P8_44 = Pin('P8_44')  # GPIO_73
P8_45 = Pin('P8_45')  # GPIO_70
P8_46 = Pin('P8_46')  # GPIO_71

# P9_1 = DGND
# P9_2 = DGND
# P9_3 = VDD_3V3
# P9_4 = VDD_3V3
# P9_5 = VDD_5V
# P9_6 = VDD_5V
# P9_7 = SYS_5V
# P9_8 = SYS_5V
# P9_9 = PWR_BUT
# P9_10 = SYS_RESETN
P9_11 = Pin('P9_11')  # GPIO_30
P9_12 = Pin('P9_12')  # GPIO_60
P9_13 = Pin('P9_13')  # GPIO_31
P9_14 = Pin('P9_14')  # GPIO_40
P9_15 = Pin('P9_15')  # GPIO_48
P9_16 = Pin('P9_16')  # GPIO_51
P9_17 = Pin('P9_17')  # GPIO_4
P9_18 = Pin('P9_18')  # GPIO_5
P9_19 = Pin('P9_19')  # I2C2_SCL
P9_20 = Pin('P9_20')  # I2C2_SDA
P9_21 = Pin('P9_21')  # GPIO_3
P9_22 = Pin('P9_22')  # GPIO_2
P9_23 = Pin('P9_23')  # GPIO_49
P9_24 = Pin('P9_24')  # GPIO_15
P9_25 = Pin('P9_25')  # GPIO_117
P9_26 = Pin('P9_26')  # GPIO_14
P9_27 = Pin('P9_27')  # GPIO_125
P9_28 = Pin('P9_28')  # GPIO_123
P9_29 = Pin('P9_29')  # GPIO_121
P9_30 = Pin('P9_30')  # GPIO_122
P9_31 = Pin('P9_31')  # GPIO_120
# P9_32 = VDD_ADC
# P9_33 = AIN4
# P9_34 = GNDA_ADC
# P9_35 = AIN6
# P9_36 = AIN5
# P9_37 = AIN2
# P9_38 = AIN3
# P9_39 = AIN0
# P9_40 = AIN1
P9_41 = Pin('P9_41')  # GPIO_20
P9_42 = Pin('P9_42')  # GPIO_7
# P9_43 = DGND
# P9_44 = DGND
# P9_45 = DGND
# P9_46 = DGND

# common to all beagles
USR0 = Pin('USR0')
USR1 = Pin('USR1')
USR2 = Pin('USR2')
USR3 = Pin('USR3')

# all special functions (SPI / I2C) are moved to
# src/adafruit_blinka/board/beaglebone_black.py

# # ordered as spiId, sckId, mosiId, misoId
# spiPorts = (
#     (0, SCLK, MOSI, MISO),
#     (1, SCLK_1, MOSI_1, MISO_1)
# )
#
# # ordered as uartId, txId, rxId
# uartPorts = (
#     (),
# )
#
# i2cPorts = (
#     (2, SCL, SDA),
# )
