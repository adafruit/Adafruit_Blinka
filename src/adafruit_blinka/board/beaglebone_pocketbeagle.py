"""
Pin definitions for the Beaglebone PocketBeagle.

based on
https://github.com/beagleboard/pocketbeagle/wiki/System-Reference-Manual#figure-42-expansion-header-popular-functions---color-coded
"""
from adafruit_blinka.microcontroller.am335x import pin

# initial pins, to mimic bonescript demo
# PocketBeagle
# P1_1 = SYS VIN        # VIN_AC
P1_2 = pin.P1_2      # GPIO2_23 - GPIO_87
P1_3 = pin.P1_3      # USB1_VBUS_OUT
P1_4 = pin.P1_4      # GPIO2_25 - GPIO_89
# P1_5 = USB VBUS       # USB1_VBUS_IN
P1_6 = pin.P1_6      # SPI0_CS0 - GPIO_5
# P1_7 = USB VIN        # VIN-USB
P1_8 = pin.P1_8      # SPI0_SCLK - GPIO_2
# P1_9 = USB1 DN        # USB1-DN
P1_10 = pin.P1_10    # SPI0_D0 - GPIO_3
# P1_11 = USB1 DP       # USB1-DP
P1_12 = pin.P1_12    # SPI0_D1 - GPIO_4
# P1_13 = USB1 ID       # USB1-ID
# P1_14 = SYS 3.3V      # VOUT-3.3V
# P1_15 = SYS GND       # GND
# P1_16 = SYS GND       # GND
# P1_17 = AIN 1.8V REF- # VREFN
# P1_18 = AIN 1.8V REF+ # VREFP
P1_19 = pin.P1_19    # AIN0
P1_20 = pin.P1_20    # GPIO0_20 - GPIO_20
P1_21 = pin.P1_21    # AIN1
# P1_22 = SYS GND       # GND
P1_23 = pin.P1_23    # AIN2
# P1_22 = SYS VOUT      # VOUT-5V
P1_25 = pin.P1_25    # AIN3
P1_26 = pin.P1_26    # I2C2_SDA - GPIO_12
P1_27 = pin.P1_27    # AIN4
P1_28 = pin.P1_28    # I2C2_SCL - GPIO_13
P1_29 = pin.P1_29    # GPIO3_21 - GPIO_117
P1_30 = pin.P1_30    # UART0_TXD - GPIO_43
P1_31 = pin.P1_31    # GPIO3_18 - GPIO_114
P1_32 = pin.P1_32    # UART0_RXD - GPIO_42
P1_33 = pin.P1_33    # GPIO3_15 - GPIO_111
P1_34 = pin.P1_34    # GPIO0_26 - GPIO_26
P1_35 = pin.P1_35    # GPIO2_24 - GPIO_88
P1_36 = pin.P1_36    # EHRPWM0A - GPIO_110


P2_1 = pin.P2_1      # EHRPWM1A - GPIO_50
P2_2 = pin.P2_2      # GPIO1_27 - GPIO_59
P2_3 = pin.P2_3      # GPIO0_23 - GPIO_23
P2_4 = pin.P2_4      # GPIO1_26 - GPIO_58
P2_5 = pin.P2_5      # UART4_RXD - GPIO_30
P2_6 = pin.P2_6      # GPIO1_25 - GPIO_57
P2_7 = pin.P2_7      # UART4_TXD - GPIO_31
P2_8 = pin.P2_8      # GPIO1_28 - GPIO_60
P2_9 = pin.P2_9      # I2C1_SCL - GPIO_15
P2_10 = pin.P2_10    # GPIO1_20 - GPIO_52
P2_11 = pin.P2_11    # I2C1_SDA - GPIO_14
# P2_12 = SYS  PWR BTN  # POWER_BUTTON
# P2_13 = SYS VOUT      # VOUT-5V
# P2_14 = BAT VIN       # BAT-VIN
# P2_15 = SYS GND       # GND
# P2_16 = BAT TEMP      # BAT-TEMP
P2_17 = pin.P2_17    # GPIO2_1 - GPIO_65
P2_18 = pin.P2_18    # GPIO1_15 - GPIO_47
P2_19 = pin.P2_19    # GPIO0_27 - GPIO_27
P2_20 = pin.P2_20    # GPIO2_0 - GPIO_64
# P2_21 = SYS GND       # GND
P2_22 = pin.P2_22    # GPIO1_14 - GPIO_46
# P2_23 = SYS 3.3V      # VOUT-3.3V
P2_24 = pin.P2_24    # GPIO1_12 - GPIO_44
P2_25 = pin.P2_25    # SPI1_CS0 - GPIO_41
# P2_26 = SYS NRST      # RESET#
P2_27 = pin.P2_27    # SPI1_D0 - GPIO_40
P2_28 = pin.P2_28    # GPIO3_20 - GPIO_116
P2_29 = pin.P2_29    # SPI1_SCLK - GPIO_7
P2_30 = pin.P2_30    # GPIO3_17 - GPIO_113
P2_31 = pin.P2_31    # SPI1_CS1 - GPIO_19
P2_32 = pin.P2_32    # GPIO3_16 - GPIO_112
P2_33 = pin.P2_33    # GPIO1_13 - GPIO_45
P2_34 = pin.P2_34    # GPIO3_19 - GPIO_115
P2_35 = pin.P2_35    # GPIO2_22 - GPIO_86
P2_36 = pin.P2_36    # AIN7

# common to all beagles
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
SDA_1 = pin.P2_11
SCL_1 = pin.P2_9

# I2C2 pins
# P1_26 (I2C2_SDA => SDA_2) data signal
# P1_28 (I2C2_SCL => SCL_2) clock signal
SDA_2 = pin.P1_26
SCL_2 = pin.P1_28

# SPI0 pins
# P1_6 (SPI0_CSO => CE0) enables peripheral device
# P1_12 (SPI0_MOSI => MOSI) outputs data to peripheral device
# P1_10 (SPIO_MISO => MISO) receives data from peripheral device
# P1_8 (SPI0_CLK => SCLK) outputs clock signal
CE0 = pin.P1_6
MOSI = pin.P1_12
MISO = pin.P1_10
SCLK = pin.P1_8
# CircuitPython naming convention for SPI Clock
SCK = SCLK

# SPI1 pins
# P2_31 (SPI1_CS1 => CE1) enables peripheral device
# P2_25 (SPI1_MOSI => MOSI) outputs data to peripheral device
# P2_27 (SPI1_MISO => MISO) receives data from peripheral device
# P2_29 (SPI1_CLK => SCLK) outputs clock signal
CE1 = pin.P2_31
MOSI_1 = pin.P2_25
MISO_1 = pin.P2_27
SCLK_1 = pin.P2_29
# CircuitPython naming convention for SPI Clock
SCK_1 = SCLK_1


# UART0
TX_0 = pin.P1_30
RX_0 = pin.P1_32

TX = TX_0
RX = RX_0


# UART2
# pins already in use by SPI0
# TX_2 = pin.P1_8
# RX_2 = pin.P1_10

# UART4
TX_4 = pin.P2_7
RX_4 = pin.P2_5


# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SCLK, MOSI, MISO),
    (1, SCLK_1, MOSI_1, MISO_1),
)

# ordered as uartId, txId, rxId
uartPorts = (
    (0, TX_0, RX_0),
    (4, TX_4, RX_4),
)

i2cPorts = (
    (1, SCL_1, SDA_1),
    (2, SCL_2, SDA_2),
)
