# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""AM335x pin names"""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin


# names in comments copied from
# https://github.com/adafruit/adafruit-beaglebone-io-python/blob/master/source/common.c#L73

# PocketBeagle
# P1_1 = SYS VIN        # VIN_AC
P1_2 = Pin((2, 23))  # GPIO2_23 - GPIO_87
P1_3 = Pin((0, 0))  # USB1_VBUS_OUT - (silkscreen: USB1 V_EN)
P1_4 = Pin((2, 25))  # GPIO2_25 - GPIO_89
# P1_5 = USB VBUS       # USB1_VBUS_IN
P1_6 = Pin((0, 5))  # SPI0_CS0 - GPIO_5
# P1_7 = USB VIN        # VIN-USB
P1_8 = Pin((0, 2))  # SPI0_SCLK - GPIO_2
# P1_9 = USB1 DN        # USB1-DN
P1_10 = Pin((0, 3))  # SPI0_D0 - GPIO_3
# P1_11 = USB1 DP       # USB1-DP
P1_12 = Pin((0, 4))  # SPI0_D1 - GPIO_4
# P1_13 = USB1 ID       # USB1-ID
# P1_14 = SYS 3.3V      # VOUT-3.3V
# P1_15 = SYS GND       # GND
# P1_16 = SYS GND       # GND
# P1_17 = AIN 1.8V REF- # VREFN
# P1_18 = AIN 1.8V REF+ # VREFP
P1_19 = Pin((0, 0))  # AIN0
P1_20 = Pin((0, 20))  # GPIO0_20 - GPIO_20
P1_21 = Pin((0, 0))  # AIN1
# P1_22 = SYS GND       # GND
P1_23 = Pin((0, 0))  # AIN2
# P1_22 = SYS VOUT      # VOUT-5V
P1_25 = Pin((0, 0))  # AIN3
P1_26 = Pin((0, 12))  # I2C2_SDA - GPIO_12
P1_27 = Pin((0, 0))  # AIN4
P1_28 = Pin((0, 13))  # I2C2_SCL - GPIO_13
P1_29 = Pin((3, 21))  # GPIO3_21 - GPIO_117
P1_30 = Pin((1, 11))  # UART0_TXD - GPIO_43
P1_31 = Pin((3, 18))  # GPIO3_18 - GPIO_114
P1_32 = Pin((1, 10))  # UART0_RXD - GPIO_42
P1_33 = Pin((3, 15))  # GPIO3_15 - GPIO_111
P1_34 = Pin((0, 26))  # GPIO0_26 - GPIO_26
P1_35 = Pin((2, 24))  # GPIO2_24 - GPIO_88
P1_36 = Pin((3, 14))  # EHRPWM0A - GPIO_110


P2_1 = Pin((1, 18))  # EHRPWM1A - GPIO_50
P2_2 = Pin((1, 27))  # GPIO1_27 - GPIO_59
P2_3 = Pin((0, 23))  # GPIO0_23 - GPIO_23
P2_4 = Pin((1, 26))  # GPIO1_26 - GPIO_58
P2_5 = Pin((0, 30))  # UART4_RXD - GPIO_30
P2_6 = Pin((1, 25))  # GPIO1_25 - GPIO_57
P2_7 = Pin((0, 31))  # UART4_TXD - GPIO_31
P2_8 = Pin((1, 28))  # GPIO1_28 - GPIO_60
P2_9 = Pin((0, 15))  # I2C1_SCL - GPIO_15
P2_10 = Pin((1, 20))  # GPIO1_20 - GPIO_52
P2_11 = Pin((0, 14))  # I2C1_SDA - GPIO_14
# P2_12 = SYS  PWR BTN  # POWER_BUTTON
# P2_13 = SYS VOUT      # VOUT-5V
# P2_14 = BAT VIN       # BAT-VIN
# P2_15 = SYS GND       # GND
# P2_16 = BAT TEMP      # BAT-TEMP
P2_17 = Pin((2, 1))  # GPIO2_1 - GPIO_65
P2_18 = Pin((1, 15))  # GPIO1_15 - GPIO_47
P2_19 = Pin((0, 27))  # GPIO0_27 - GPIO_27
P2_20 = Pin((2, 0))  # GPIO2_0 - GPIO_64
# P2_21 = SYS GND       # GND
P2_22 = Pin((1, 14))  # GPIO1_14 - GPIO_46
# P2_23 = SYS 3.3V      # VOUT-3.3V
P2_24 = Pin((1, 12))  # GPIO1_12 - GPIO_44
P2_25 = Pin((1, 9))  # SPI1_D1 - GPIO_41
# P2_26 = SYS NRST      # RESET#
P2_27 = Pin((1, 8))  # SPI1_D0 - GPIO_40
P2_28 = Pin((3, 20))  # GPIO3_20 - GPIO_116
P2_29 = Pin((0, 7))  # SPI1_SCLK - GPIO_7
P2_30 = Pin((3, 17))  # GPIO3_17 - GPIO_113
P2_31 = Pin((0, 19))  # SPI1_CS1 - GPIO_19
P2_32 = Pin((3, 16))  # GPIO3_16 - GPIO_112
P2_33 = Pin((1, 13))  # GPIO1_13 - GPIO_45
P2_34 = Pin((3, 19))  # GPIO3_19 - GPIO_115
P2_35 = Pin((2, 22))  # GPIO2_22 - GPIO_86
P2_36 = Pin((0, 0))  # AIN7


# BeagleBone Black
# P8_1 = DGND           # DGND - GPIO_0
# P8_2 = DGND           # DGND - GPIO_0
P8_3 = Pin((1, 6))  # GPIO1_6 - GPIO_38
P8_4 = Pin((1, 7))  # GPIO1_7 - GPIO_39
P8_5 = Pin((1, 2))  # GPIO1_2 - GPIO_34
P8_6 = Pin((1, 3))  # GPIO1_3 - GPIO_35
P8_7 = Pin((2, 2))  # TIMER4 - GPIO_66
P8_8 = Pin((2, 3))  # TIMER7 - GPIO_67
P8_9 = Pin((2, 5))  # TIMER5 - GPIO_69
P8_10 = Pin((2, 4))  # TIMER6 - GPIO_68
P8_11 = Pin((1, 13))  # GPIO1_13 - GPIO_45
P8_12 = Pin((1, 12))  # GPIO1_12 - GPIO_44
P8_13 = Pin((0, 23))  # EHRPWM2B - GPIO_23
P8_14 = Pin((0, 26))  # GPIO0_26 - GPIO_26
P8_15 = Pin((1, 15))  # GPIO1_15 - GPIO_47
P8_16 = Pin((1, 14))  # GPIO1_14 - GPIO_46
P8_17 = Pin((0, 27))  # GPIO0_27 - GPIO_27
P8_18 = Pin((2, 1))  # GPIO2_1 - GPIO_65
P8_19 = Pin((0, 22))  # EHRPWM2A - GPIO_22
P8_20 = Pin((1, 31))  # GPIO1_31 - GPIO_63
P8_21 = Pin((1, 30))  # GPIO1_30 - GPIO_62
P8_22 = Pin((1, 5))  # GPIO1_5 - GPIO_37
P8_23 = Pin((1, 4))  # GPIO1_4 - GPIO_36
P8_24 = Pin((1, 1))  # GPIO1_1 - GPIO_33
P8_25 = Pin((1, 0))  # GPIO1_0 - GPIO_32
P8_26 = Pin((1, 29))  # GPIO1_29 - GPIO_61
P8_27 = Pin((2, 22))  # GPIO2_22 - GPIO_86
P8_28 = Pin((2, 24))  # GPIO2_24 - GPIO_88
P8_29 = Pin((2, 23))  # GPIO2_23 - GPIO_87
P8_30 = Pin((2, 25))  # GPIO2_25 - GPIO_89
P8_31 = Pin((0, 10))  # UART5_CTSN - GPIO_10
P8_32 = Pin((0, 11))  # UART5_RTSN - GPIO_11
P8_33 = Pin((0, 9))  # UART4_RTSN - GPIO_9
P8_34 = Pin((2, 17))  # UART3_RTSN - GPIO_81
P8_35 = Pin((0, 8))  # UART4_CTSN - GPIO_8
P8_36 = Pin((2, 16))  # UART3_CTSN - GPIO_80
P8_37 = Pin((2, 14))  # UART5_TXD - GPIO_78
P8_38 = Pin((2, 15))  # UART5_RXD - GPIO_79
P8_39 = Pin((2, 12))  # GPIO2_12 - GPIO_76
P8_40 = Pin((2, 13))  # GPIO2_13 - GPIO_77
P8_41 = Pin((2, 10))  # GPIO2_10 - GPIO_74
P8_42 = Pin((2, 11))  # GPIO2_11 - GPIO_75
P8_43 = Pin((2, 8))  # GPIO2_8 - GPIO_72
P8_44 = Pin((2, 9))  # GPIO2_9 - GPIO_73
P8_45 = Pin((2, 6))  # GPIO2_6 - GPIO_70
P8_46 = Pin((2, 7))  # GPIO2_7 - GPIO_71

# P9_1 = DGND           # DGND - GPIO_0
# P9_2 = DGND           # DGND - GPIO_0
# P9_3 = VDD_3V3        # VDD_3V3 - GPIO_0
# P9_4 = VDD_3V3        # VDD_3V3 - GPIO_0
# P9_5 = VDD_5V         # VDD_5V - GPIO_0
# P9_6 = VDD_5V         # VDD_5V - GPIO_0
# P9_7 = SYS_5V         # SYS_5V - GPIO_0
# P9_8 = SYS_5V         # SYS_5V - GPIO_0
# P9_9 = PWR_BUT        # PWR_BUT - GPIO_0
# P9_10 = SYS_RESETN    # SYS_RESETn - GPIO_0
P9_11 = Pin((0, 30))  # GPIO0_30 - GPIO_30
P9_12 = Pin((1, 28))  # GPIO1_28 - GPIO_60
P9_13 = Pin((0, 31))  # GPIO0_31 - GPIO_31
P9_14 = Pin((1, 18))  # GPIO1_18 - GPIO_50
P9_15 = Pin((1, 16))  # GPIO1_16 - GPIO_48
P9_16 = Pin((1, 19))  # GPIO1_19 - GPIO_51
P9_17 = Pin((0, 5))  # GPIO0_5  - GPIO_5
P9_18 = Pin((0, 4))  # GPIO0_4  - GPIO_4
P9_19 = Pin((0, 13))  # GPIO0_13 - GPIO_13
P9_20 = Pin((0, 12))  # GPIO0_12 - GPIO_12
P9_21 = Pin((0, 3))  # GPIO0_3  - GPIO_3
P9_22 = Pin((0, 2))  # GPIO0_2  - GPIO_2
P9_23 = Pin((1, 17))  # GPIO1_17 - GPIO_49
P9_24 = Pin((0, 15))  # GPIO0_15 - GPIO_15
P9_25 = Pin((3, 21))  # GPIO3_21 - GPIO_117
P9_26 = Pin((0, 14))  # GPIO0_14 - GPIO_14
P9_27 = Pin((3, 19))  # GPIO3_19 - GPIO_115
P9_28 = Pin((3, 17))  # GPIO3_17 - GPIO_113
P9_29 = Pin((3, 15))  # GPIO3_15 - GPIO_111
P9_30 = Pin((3, 16))  # GPIO3_16 - GPIO_112
P9_31 = Pin((3, 14))  # GPIO3_14 - GPIO_110
# P9_32 = VDD_ADC       # VDD_ADC - GPIO_0
# P9_33 = AIN4          # AIN4 - GPIO_0
# P9_34 = GNDA_ADC      # GNDA_ADC - GPIO_0
# P9_35 = AIN6          # AIN6 - GPIO_0
# P9_36 = AIN5          # AIN5 - GPIO_0
# P9_37 = AIN2          # AIN2 - GPIO_0
# P9_38 = AIN3          # AIN3 - GPIO_0
# P9_39 = AIN0          # AIN0 - GPIO_0
# P9_40 = AIN1          # AIN1 - GPIO_0
P9_41 = Pin((0, 20))  # GPIO0_20 - GPIO_20
P9_42 = Pin((0, 7))  # GPIO0_7  - GPIO_7
# P9_43 = DGND          # DGND - GPIO_0
# P9_44 = DGND          # DGND - GPIO_0
# P9_45 = DGND          # DGND - GPIO_0
# P9_46 = DGND          # DGND - GPIO_0


##########################################
# common to all beagles
USR0 = Pin((1, 21))  # USR0 - GPIO_53
USR1 = Pin((1, 22))  # USR1 - GPIO_54
USR2 = Pin((1, 23))  # USR2 - GPIO_55
USR3 = Pin((1, 24))  # USR3 - GPIO_56


##########################################
# specials

# analog input
# AIN0 = Pin("AIN0")
# AIN1 = Pin("AIN1")
# AIN2 = Pin("AIN2")
# AIN3 = Pin("AIN3")
# AIN4 = Pin("AIN4")
# AIN5 = Pin("AIN5")
# AIN6 = Pin("AIN6")
# AIN7 = Pin("AIN7")

# PWM
# EHRPWM0A = Pin("EHRPWM0A")
# EHRPWM0B = Pin("EHRPWM0B")
EHRPWM1A = P9_14
EHRPWM1B = P9_16
EHRPWM2A = P8_19
EHRPWM2B = P8_13
# ECAPPWM0 = Pin("ECAPPWM0")
# ECAPPWM2 = Pin("ECAPPWM2")
TIMER4 = P8_7
TIMER5 = P8_9
TIMER6 = P8_10
TIMER7 = P8_8


# I2C1
I2C1_SDA = P2_11
I2C1_SCL = P2_9

# I2C2
I2C2_SDA = P1_26
I2C2_SCL = P1_28

# SPI0
SPI0_CS0 = P9_17
SPI0_SCLK = P9_22
SPI0_D1 = P9_18
SPI0_D0 = P9_22

# SPI1
SPI1_CS0 = P9_28
SPI1_CS1 = P2_31
SPI1_SCLK = P2_29
SPI1_D1 = P2_25
SPI1_D0 = P2_27

# UART0
UART0_TXD = P1_30
UART0_RXD = P1_32

# UART1
UART1_TXD = P9_24
UART1_RXD = P9_26
# UART1_RTSn = Pin("UART1_RTSn")
# UART1_CTSn = Pin("UART1_CTSn")

# UART2
UART2_TXD = P9_21
UART2_RXD = P9_22

# UART3
# UART3_TXD = Pin("UART3_TXD")
# UART3_RXD = Pin("UART3_RXD")
UART3_RTSn = P8_34
UART3_CTSn = P8_36

# UART4
UART4_TXD = P9_13
UART4_RXD = P9_11
UART4_RTSn = P8_33
UART4_CTSn = P8_35

# UART5
UART5_TXD = P8_37
UART5_RXD = P8_38
UART5_RTSn = P8_32
UART5_CTSn = P8_31


# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SPI0_SCLK, SPI0_D1, SPI0_D0),
    (1, SPI1_SCLK, SPI1_D1, SPI1_D0),
)

# ordered as uartId, txId, rxId
uartPorts = (
    # (0, UART0_TXD, UART0_RXD),
    # (1, UART1_TXD, UART1_RXD),
    # (2, UART2_TXD, UART2_RXD),
    # (4, UART4_TXD, UART4_RXD),
    # (5, UART5_TXD, UART5_RXD),
)

# ordered as i2cId, SCL, SDA
i2cPorts = (
    (1, I2C1_SCL, I2C1_SDA),
    (2, I2C2_SCL, I2C2_SDA),
)

PWM1 = P1_36
PWM2 = P1_33
PWM3 = P2_1
PWM4 = P2_3

pwmOuts = (((0, 0), PWM1), ((0, 1), PWM2), ((2, 0), PWM3), ((4, 1), PWM4))
