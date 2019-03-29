"""Pin definitions for the Beaglebone Black."""
from adafruit_blinka.microcontroller.am335x import pin

# initial pins, to mimic bonescript demo
P8_3 = pin.P8_3
P8_4 = pin.P8_4
P8_5 = pin.P8_5
P8_6 = pin.P8_6
P8_7 = pin.P8_7
P8_8 = pin.P8_8
P8_9 = pin.P8_9
P8_10 = pin.P8_10
P8_11 = pin.P8_11
P8_12 = pin.P8_12
P8_13 = pin.P8_13
P8_14 = pin.P8_14
P8_15 = pin.P8_15
P8_16 = pin.P8_16
P8_17 = pin.P8_17
P8_18 = pin.P8_18
P8_19 = pin.P8_19
P8_20 = pin.P8_20
P8_21 = pin.P8_21
P8_22 = pin.P8_22
P8_23 = pin.P8_23
P8_24 = pin.P8_24
P8_25 = pin.P8_25
P8_26 = pin.P8_26
P8_27 = pin.P8_27
P8_28 = pin.P8_28
P8_29 = pin.P8_29
P8_30 = pin.P8_30
P8_31 = pin.P8_31
P8_32 = pin.P8_32
P8_33 = pin.P8_33
P8_34 = pin.P8_34
P8_35 = pin.P8_35
P8_36 = pin.P8_36
P8_37 = pin.P8_37
P8_38 = pin.P8_38
P8_39 = pin.P8_39
P8_40 = pin.P8_40
P8_41 = pin.P8_41
P8_42 = pin.P8_42
P8_43 = pin.P8_43
P8_44 = pin.P8_44
P8_45 = pin.P8_45
P8_46 = pin.P8_46
P9_11 = pin.P9_11
P9_12 = pin.P9_12
P9_13 = pin.P9_13
P9_14 = pin.P9_14
P9_15 = pin.P9_15
P9_16 = pin.P9_16
P9_17 = pin.P9_17
P9_18 = pin.P9_18
P9_19 = pin.P9_19
P9_20 = pin.P9_20
P9_21 = pin.P9_21
P9_22 = pin.P9_22
P9_23 = pin.P9_23
P9_24 = pin.P9_24
P9_25 = pin.P9_25
P9_26 = pin.P9_26
P9_27 = pin.P9_27
P9_28 = pin.P9_28
P9_29 = pin.P9_29
P9_30 = pin.P9_30
P9_31 = pin.P9_31
P9_41 = pin.P9_41
P9_42 = pin.P9_42

LED_USR0 = pin.USR0
LED_USR1 = pin.USR1
LED_USR2 = pin.USR2
LED_USR3 = pin.USR3

# I2C and SPI pins from:
# src/adafruit_blinka/board/raspi_40pin.py
# SDA = pin.SDA
# SCL = pin.SCL
# CE1 = pin.D7
# CE0 = pin.D8
# MISO = pin.D9
# MOSI = pin.D10
# SCLK = pin.D11
# SCK = pin.D11
# TXD = pin.D14
# RXD = pin.D15
# MISO_1 = pin.D19
# MOSI_1 = pin.D20
# SCLK_1 = pin.D21
# SCK_1 = pin.D21

SDA = pin.P9_19
SCL = pin.P9_20

# Refer to header default pin modes
# http://beagleboard.org/static/images/cape-headers.png
#
# P9_17 (SPI0_CSO => CE0) enables peripheral device
# P9_18 (SPI0_D1 => MOSI) outputs data to peripheral device
# P9_21 (SPIO_DO => MISO) receives data from peripheral device
# P9_22 (SPI0_SCLK => SCLK) outputs clock signal
#
# Use config-pin to set pin mode for SPI pins
# https://github.com/beagleboard/bb.org-overlays/tree/master/tools/beaglebone-universal-io
# config-pin p9.17 spi_cs
# config-pin p9.18 spi
# config-pin p9.21 spi
# config-pin p9.22 spi_sclk
#
CE0 = pin.P9_17
MOSI = pin.P9_18
MISO = pin.P9_21
SCLK = pin.P9_22
# CircuitPython naming convention for SPI Clock
SCK = SCLK

# Pins for SPI1
# refer to:
# http://beagleboard.org/static/images/cape-headers-spi.png
#
# CE1 P9.28 SPI1_CS0
# MISO_1 P9.29 SPI1_D0
# MOSI_1 P9.30 SPI1_D1
# SCLK_1 P9.31 SPI_SCLK
#
# SPI1 conflicts with HDMI Audio (McASP)
#
# Refer to:
# https://elinux.org/Beagleboard:BeagleBoneBlack_Debian#U-Boot_Overlays
#
# To Disable HDMI AUDIO, uncomment this line in /boot/uEnv.txt:
# disable_uboot_overlay_audio=1
#
# Set pin modes for SPI1 with:
#
# config-pin p9.28 spi1_cs
# config-pin p9.29 spi1
# config-pin p9.30 spi1
# config-pin p9.31 spi_sclk
CE1 = pin.P9_28
MOSI_1 = pin.P9_29
MISO_1 = pin.P9_30
SCLK_1 = pin.P9_31
# CircuitPython naming convention for SPI Clock
SCK_1 = SCLK_1


# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SCLK, MOSI, MISO),
    (1, SCLK_1, MOSI_1, MISO_1)
)

# ordered as uartId, txId, rxId
uartPorts = (
    (),
)

i2cPorts = (
    (2, SCL, SDA),
)
