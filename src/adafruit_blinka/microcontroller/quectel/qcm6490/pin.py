# SPDX-FileCopyrightText: 2025 Brett Walach for Particle
#
# SPDX-License-Identifier: MIT
"""Quectel QCM6490 pin names"""

from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin as GenericLinuxPin

import os

# Release (unexport)  all pins on init and set to INPUT mode
class Pin(GenericLinuxPin):
    def __init__(self, pin_id):
        self._release_sysfs_gpio(pin_id)
        super().__init__(pin_id)

    def _release_sysfs_gpio(self, pin_id, base_offset=336):
        # pin_id might be a tuple like (chip_id, line_number)
        if isinstance(pin_id, tuple):
            _, line_number = pin_id
        else:
            line_number = pin_id

        gpio_num = base_offset + int(line_number)
        gpio_path = f"/sys/class/gpio/gpio{gpio_num}"

        try:
            if not os.path.exists(gpio_path):
                with open("/sys/class/gpio/export", "w") as f:
                    f.write(f"{gpio_num}")
            with open(f"{gpio_path}/direction", "w") as f:
                f.write("in")
            with open("/sys/class/gpio/unexport", "w") as f:
                f.write(f"{gpio_num}")
        except Exception:
            # fail silently if not allowed
            pass

# Use with sysfs_pin
# GPIO_BASE = 336

# Use with libgpiod_pin
GPIO_BASE = 0

GPIO_6 = Pin(GPIO_BASE + 6)
UART01_TXD = GPIO_6
PWM1 = GPIO_6

GPIO_8 = Pin(GPIO_BASE + 8)
I2C02_SDA = GPIO_8
SDA = GPIO_8

GPIO_9 = Pin(GPIO_BASE + 9)
I2C02_SCL = GPIO_9
SCL = GPIO_9

GPIO_18 = Pin(GPIO_BASE + 18)
UART04_TXD = GPIO_18
SPI04_CLK = GPIO_18

GPIO_19 = Pin(GPIO_BASE + 19)
UART04_RXD = GPIO_19
SPI04_CS0 = GPIO_19

GPIO_24 = Pin(GPIO_BASE + 24)

GPIO_32 = Pin(GPIO_BASE + 32)
UART10_CTS = GPIO_32
CTS = GPIO_32

GPIO_33 = Pin(GPIO_BASE + 33)
UART10_RTS = GPIO_33
RTS = GPIO_33

GPIO_34 = Pin(GPIO_BASE + 34)
UART10_TXD = GPIO_34

GPIO_35 = Pin(GPIO_BASE + 35)
UART10_RXD = GPIO_35

GPIO_36 = Pin(GPIO_BASE + 36)
UART11_CTS = GPIO_36
SPI11_MISO = GPIO_36
I2C11_SDA = GPIO_36
EEPROM_SDA = GPIO_36

GPIO_37 = Pin(GPIO_BASE + 37)
UART11_RTS = GPIO_37
SPI11_MOSI = GPIO_37
I2C11_SCL = GPIO_37
EEPROM_SCL = GPIO_37

GPIO_40 = Pin(GPIO_BASE + 40)
QWIIC_I2C12_SDA = GPIO_40

GPIO_41 = Pin(GPIO_BASE + 41)
QWIIC_I2C12_SCL = GPIO_41

GPIO_44 = Pin(GPIO_BASE + 44)

GPIO_56 = Pin(GPIO_BASE + 56)
SPI16_MISO = GPIO_56
I2C16_SDA = GPIO_56
UART16_CTS = GPIO_56
MISO = GPIO_56

GPIO_57 = Pin(GPIO_BASE + 57)
SPI16_MOSI = GPIO_57
I2C16_SCL = GPIO_57
UART16_RTS = GPIO_57
MOSI = GPIO_57

GPIO_58 = Pin(GPIO_BASE + 58)
SPI16_CLK = GPIO_58
UART16_TXD = GPIO_58
SCK = GPIO_58

GPIO_59 = Pin(GPIO_BASE + 59)
SPI16_CS0 = GPIO_59
UART16_RXD = GPIO_59
CE0 = GPIO_59

GPIO_61 = Pin(GPIO_BASE + 61)

GPIO_62 = Pin(GPIO_BASE + 62)
SPI16_CS1 = GPIO_62
CE1 = GPIO_62

GPIO_78 = Pin(GPIO_BASE + 78)
PWM0 = GPIO_78

GPIO_106 = Pin(GPIO_BASE + 106)
MI2S1_SCLK = GPIO_106
PWM = GPIO_106
PWM1 = GPIO_106

GPIO_144 = Pin(GPIO_BASE + 144)
LPI_MI2S_SCLK = GPIO_144

GPIO_145 = Pin(GPIO_BASE + 145)
LPI_MI2S_WS = GPIO_145
MISO1 = GPIO_145

GPIO_146 = Pin(GPIO_BASE + 146)
LPI_MI2S_DATA0 = GPIO_146
MOSI1 = GPIO_146

GPIO_147 = Pin(GPIO_BASE + 147)
LPI_MI2S_DATA1 = GPIO_147
SCK1 = GPIO_147

GPIO_158 = Pin(GPIO_BASE + 158)

GPIO_165 = Pin(GPIO_BASE + 165)

GPIO_166 = Pin(GPIO_BASE + 166)

# ordered as i2cId, i2cSclId, i2cSdaId
i2cPorts = (
    (1, I2C02_SCL, I2C02_SDA),
    (2, QWIIC_I2C12_SCL, QWIIC_I2C12_SDA),
)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (0, SPI16_CLK, SPI16_MOSI, SPI16_MISO),
    (1, SPI16_CLK, SPI16_MOSI, SPI16_MISO)
)

# ordered as uartId, txId, rxId
uartPorts = ((10, UART10_TXD, UART10_RXD),)

# ordered as pwmChipId, pwmChannelId, pwmId
pwmOuts = (((0, 0), PWM1),)
