# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""Pin definitions for the LubanCat STM32MP157."""

from adafruit_blinka.microcontroller.stm32.stm32mp157 import pin

# Pro board pin header J1 named GPIO_PAx, pin header J2 named GPIO_PBx

# Board pin name [= alias] = RPI name [= alias] = pin name

# connector J1
GPIO_PA3 = USART1_CTS = PZ3 = pin.PZ3
GPIO_PA4 = USART1_RTS = PZ5 = pin.PZ5
GPIO_PA5 = USART1_TX = PZ7 = pin.PZ7
GPIO_PA6 = USART1_RX = PZ6 = pin.PZ6
GPIO_PA7 = USART3_TX = PB10 = pin.PB10
GPIO_PA8 = USART3_RX = PB12 = pin.PB12
GPIO_PA11 = FDCAN1_TX = PA12 = pin.PA12
GPIO_PA12 = FDCAN1_RX = PA11 = pin.PA11
# connector J2
GPIO_PB7 = UART4_TX = PG11 = pin.PG11
GPIO_PB8 = UART4_RX = PB2 = pin.PB2
GPIO_PB11 = QSPI_IO0 = PF8 = pin.PF8
GPIO_PB12 = QSPI_IO1 = PF9 = pin.PF9
GPIO_PB13 = QSPI_IO2 = PF7 = pin.PF7
GPIO_PB14 = QSPI_IO3 = PF6 = pin.PF6
GPIO_PB15 = QSPI_CLK = PF10 = pin.PF10
GPIO_PB16 = QSPI_NCS = PB6 = pin.PB6

# general gpio as LED、KEY function
# LED
LED_RED = PA13 = pin.PA13
LED_GREEN = PB5 = pin.PG2
LED_BLUE = PB5 = pin.PB5
# KEY
KEY1 = PB13 = pin.PB13
KEY2 = PH7 = pin.PH7
# BEEP
BEEP = PC13 = pin.PC13

# general gpio as I2C function
# I2C1
GPIO_PA13 = I2C1_SCL = SCL1 = SCL = pin.PF14
GPIO_PA14 = I2C1_SDA = SDA1 = SDA = pin.PF15
# I2C2
GPIO_PA15 = I2C2_SCL = SCL2 = pin.PZ0
GPIO_PA16 = I2C2_SDA = SDA2 = pin.PZ1

# general gpio as analog input function
GPIO_PB3 = ADC_IN0 = ANA0 = A0 = pin.PAN0
GPIO_PB4 = ADC_IN1 = ANA1 = A1 = pin.PAN1
