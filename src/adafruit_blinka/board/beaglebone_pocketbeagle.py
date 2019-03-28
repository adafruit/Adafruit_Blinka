"""
Pin definitions for the Beaglebone PocketBeagle.

based on
https://github.com/beagleboard/pocketbeagle/wiki/System-Reference-Manual#figure-42-expansion-header-popular-functions---color-coded
"""
from adafruit_blinka.microcontroller.am335x import pin

# initial pins, to mimic bonescript demo
P1_2 = pin.P1_2
P1_3 = pin.P1_3
P1_4 = pin.P1_4

P1_6 = pin.P1_6

P1_8 = pin.P1_8

P1_10 = pin.P1_10

P1_12 = pin.P1_12

P1_19 = pin.P1_19
P1_20 = pin.P1_20
P1_21 = pin.P1_21

P1_23 = pin.P1_23

P1_25 = pin.P1_25
P1_26 = pin.P1_26
P1_27 = pin.P1_27
P1_28 = pin.P1_28
P1_29 = pin.P1_29
P1_30 = pin.P1_30
P1_31 = pin.P1_31
P1_32 = pin.P1_32
P1_33 = pin.P1_33
P1_34 = pin.P1_34
P1_35 = pin.P1_35
P1_36 = pin.P1_36


P2_1 = pin.P2_1
P2_2 = pin.P2_2
P2_3 = pin.P2_3
P2_4 = pin.P2_4
P2_5 = pin.P2_5
P2_6 = pin.P2_6
P2_7 = pin.P2_7
P2_8 = pin.P2_8
P2_9 = pin.P2_9
P2_10 = pin.P2_10
P2_11 = pin.P2_11

P2_17 = pin.P2_17
P2_18 = pin.P2_18
P2_19 = pin.P2_19
P2_20 = pin.P2_20

P2_22 = pin.P2_22

P2_24 = pin.P2_24

P2_26 = pin.P2_26
P2_27 = pin.P2_27
P2_28 = pin.P2_28
P2_29 = pin.P2_29
P2_30 = pin.P2_30
P2_31 = pin.P2_31
P2_32 = pin.P2_32
P2_33 = pin.P2_33
P2_34 = pin.P2_34
P2_35 = pin.P2_35
P2_36 = pin.P2_36

LED_USR0 = pin.USR0
LED_USR1 = pin.USR1
LED_USR2 = pin.USR2
LED_USR3 = pin.USR3

##########
# Refer to header default pin modes
# https://raw.githubusercontent.com/wiki/beagleboard/pocketbeagle/images/PocketBeagle_pinout.png

# I2C1 pins
# P2_11 (I2C1_SDA => SDA_1) data signal
# P2_9 (I2C1_SCL => SCL_1) clock signal
SDA_1 = pin.SDA_1
SCL_1 = pin.SCL_1

# I2C2 pins
# P1_26 (I2C2_SDA => SDA_2) data signal
# P1_28 (I2C2_SCL => SCL_2) clock signal
SDA_2 = pin.SDA_2
SCL_2 = pin.SCL_2

# SPI0 pins
# P1_6 (SPI0_CSO => CE0) enables peripheral device
# P1_12 (SPI0_MOSI => MOSI) outputs data to peripheral device
# P1_10 (SPIO_MISO => MISO) receives data from peripheral device
# P1_8 (SPI0_CLK => SCLK) outputs clock signal
CE0 = pin.CE0
MOSI = pin.MOSI
MISO = pin.MISO
SCLK = pin.SCLK
# CircuitPython naming convention for SPI Clock
SCK = pin.SCK

# SPI1 pins
# P2_31 (SPI1_CS1 => CE1) enables peripheral device
# P2_25 (SPI1_MOSI => MOSI) outputs data to peripheral device
# P2_27 (SPI1_MISO => MISO) receives data from peripheral device
# P2_29 (SPI1_CLK => SCLK) outputs clock signal
CE1 = pin.CE1
MOSI_1 = pin.MOSI_1
MISO_1 = pin.MISO_1
SCLK_1 = pin.SCLK_1
# CircuitPython naming convention for SPI Clock
SCK_1 = pin.SCK_1
