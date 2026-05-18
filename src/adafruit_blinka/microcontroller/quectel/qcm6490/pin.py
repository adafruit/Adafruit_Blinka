# SPDX-FileCopyrightText: 2025 Brett Walach for Particle
#
# SPDX-License-Identifier: MIT
"""Quectel QCM6490 pin names"""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# All 40-pin header GPIOs are on gpiochip4 (the main QCM6490 GPIO controller,
# 176 lines).  gpiochip0 only has 12 lines, so any GPIO number above 11 fails
# if we open chip 0.
#
# libgpiod 2.x: Pin((chip, line)) is the standard way to specify a chip.
# libgpiod 1.x: Pin((chip, line)) also works via OPEN_BY_NUMBER in
#               libgpiod_pin_1_x.py, so tuples are safe for both versions.
# Plain Pin(n) always opens gpiochip0 — do NOT use that form here.
try:
    import gpiod as _gpiod
    _GPIOD_V1 = getattr(_gpiod, "__version__", "1.").startswith("1.")
except ImportError:
    _GPIOD_V1 = True

GPIO_CHIP = 4   # gpiochip4 is the main QCM6490 GPIO bank
GPIO_BASE = 0   # kept for reference only


def _pin(line):
    """Return the correct Pin for a QCM6490 GPIO line number.

    Both gpiod 1.x (via OPEN_BY_NUMBER) and 2.x support the (chip, line)
    tuple form, so the logic is the same for both versions.  The branch is
    kept explicit so it is easy to diverge if a future gpiod version needs
    different treatment.
    """
    if _GPIOD_V1:
        # 1.x: (chip_number, line_number) tuple — opens via OPEN_BY_NUMBER
        return Pin((GPIO_CHIP, line))
    # 2.x: (chip_number, line_number) tuple — opens /dev/gpiochip{chip}
    return Pin((GPIO_CHIP, line))


GPIO_6 = _pin(6)
UART01_TXD = GPIO_6
PWM1 = GPIO_6

GPIO_8 = _pin(8)
I2C02_SDA = GPIO_8
SDA = GPIO_8

GPIO_9 = _pin(9)
I2C02_SCL = GPIO_9
SCL = GPIO_9

GPIO_18 = _pin(18)
UART04_TXD = GPIO_18
SPI04_CLK = GPIO_18

GPIO_19 = _pin(19)
UART04_RXD = GPIO_19
SPI04_CS0 = GPIO_19

GPIO_24 = _pin(24)

GPIO_32 = _pin(32)
UART10_CTS = GPIO_32
CTS = GPIO_32

GPIO_33 = _pin(33)
UART10_RTS = GPIO_33
RTS = GPIO_33

GPIO_34 = _pin(34)
UART10_TXD = GPIO_34

GPIO_35 = _pin(35)
UART10_RXD = GPIO_35

GPIO_36 = _pin(36)
UART11_CTS = GPIO_36
SPI11_MISO = GPIO_36
I2C11_SDA = GPIO_36
EEPROM_SDA = GPIO_36

GPIO_37 = _pin(37)
UART11_RTS = GPIO_37
SPI11_MOSI = GPIO_37
I2C11_SCL = GPIO_37
EEPROM_SCL = GPIO_37

GPIO_40 = _pin(40)
QWIIC_I2C12_SDA = GPIO_40

GPIO_41 = _pin(41)
QWIIC_I2C12_SCL = GPIO_41

GPIO_44 = _pin(44)

GPIO_56 = _pin(56)
SPI16_MISO = GPIO_56
I2C16_SDA = GPIO_56
UART16_CTS = GPIO_56
MISO = GPIO_56

GPIO_57 = _pin(57)
SPI16_MOSI = GPIO_57
I2C16_SCL = GPIO_57
UART16_RTS = GPIO_57
MOSI = GPIO_57

GPIO_58 = _pin(58)
SPI16_CLK = GPIO_58
UART16_TXD = GPIO_58
SCK = GPIO_58

GPIO_59 = _pin(59)
SPI16_CS0 = GPIO_59
UART16_RXD = GPIO_59
CE0 = GPIO_59

GPIO_61 = _pin(61)

GPIO_62 = _pin(62)
SPI16_CS1 = GPIO_62
CE1 = GPIO_62

GPIO_78 = _pin(78)
PWM0 = GPIO_78

GPIO_106 = _pin(106)
MI2S1_SCLK = GPIO_106
PWM = GPIO_106
PWM1 = GPIO_106

GPIO_144 = _pin(144)
LPI_MI2S_SCLK = GPIO_144

GPIO_145 = _pin(145)
LPI_MI2S_WS = GPIO_145
MISO1 = GPIO_145

GPIO_146 = _pin(146)
LPI_MI2S_DATA0 = GPIO_146
MOSI1 = GPIO_146

GPIO_147 = _pin(147)
LPI_MI2S_DATA1 = GPIO_147
SCK1 = GPIO_147

GPIO_158 = _pin(158)

GPIO_165 = _pin(165)

GPIO_166 = _pin(166)

# ordered as i2cId, i2cSclId, i2cSdaId
i2cPorts = (
    (1, I2C02_SCL, I2C02_SDA),
    (2, QWIIC_I2C12_SCL, QWIIC_I2C12_SDA),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SPI16_CLK, SPI16_MOSI, SPI16_MISO),
    (1, SPI16_CLK, SPI16_MOSI, SPI16_MISO),
)

# ordered as uartId, txId, rxId
uartPorts = ((10, UART10_TXD, UART10_RXD),)

# ordered as pwmChipId, pwmChannelId, pwmId
pwmOuts = (((0, 0), PWM1),)
