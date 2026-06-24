# SPDX-FileCopyrightText: 2025 Brett Walach for Particle
#
# SPDX-License-Identifier: MIT
"""Quectel QCM6490 pin names"""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

# The QCM6490's main 40-pin header GPIO bank (f100000.pinctrl, 176 lines) may
# appear as different gpiochip numbers depending on the kernel/BSP version:
#
#   Ubuntu 20.04 BSP : f100000.pinctrl == gpiochip0  → plain Pin(n) works
#   Current BSP      : f100000.pinctrl == gpiochip4  → must use Pin((4, n))
#
# Both Blinka libgpiod layers (1.x and 2.x) support the (chip, line) tuple
# form, so we use it unconditionally once we know the chip number.  We detect
# the chip at import time by scanning /sys/class/gpio labels so the same file
# works on both BSP generations without modification.

_TARGET_LABEL = "f100000.pinctrl"


def _find_qcm6490_chip():
    """Return the gpiochip number whose label is 'f100000.pinctrl'.

    Tries gpiod.ChipIter() (gpiod 1.x) first, then falls back to probing
    /dev/gpiochipN directly (gpiod 2.x).  Returns 0 if the main bank is
    not found — preserves Ubuntu 20.04 behaviour where f100000.pinctrl
    was enumerated as gpiochip0.
    """
    try:
        import gpiod as _gpiod
    except ImportError:
        return 0

    if hasattr(_gpiod, "ChipIter"):
        # gpiod 1.x: iterate all chips cheaply
        try:
            for _chip in _gpiod.ChipIter():
                try:
                    if _chip.label() == _TARGET_LABEL:
                        return int(_chip.name().replace("gpiochip", ""))
                finally:
                    _chip.close()
        except (AttributeError, OSError):
            return 0
        return 0

    # gpiod 2.x: probe /dev/gpiochipN until the device is missing
    for _n in range(16):
        try:
            _chip = _gpiod.Chip(f"/dev/gpiochip{_n}")
            try:
                if _chip.get_info().label == _TARGET_LABEL:
                    return _n
            finally:
                _chip.close()
        except (AttributeError, OSError):
            break
    return 0  # fallback: chip 0 (Ubuntu 20.04 layout)


GPIO_CHIP = _find_qcm6490_chip()
GPIO_BASE = 0  # kept for reference only


def _pin(line):
    """Return the correct Pin for a QCM6490 GPIO line number.

    Uses Pin((GPIO_CHIP, line)) so both gpiod 1.x (OPEN_BY_NUMBER) and
    2.x (/dev/gpiochipN path) open the right chip regardless of whether
    the main bank landed on chip 0 or chip 4.
    """
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
