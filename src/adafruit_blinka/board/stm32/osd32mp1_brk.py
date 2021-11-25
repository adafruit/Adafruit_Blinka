"""Pin definitions for the Octavo OSD32MP1 BRK board."""

# See: https://octavosystems.com/octavosystems.com/wp-content/uploads/2020/05/Default-Pin-Mapping.pdf  # pylint: disable=line-too-long

from adafruit_blinka.microcontroller.stm32.stm32mp157 import pin

# Board pin name = OSD32MP1 pin name = STM32MP1 pin name

# fmt: off
# --------------------------------
# Header Location A
# --------------------------------
# VIN - VIN                    A01
ADC_IN0 = ANA0 = pin.PAN0    # A02
TIM8_CH2 = PI6 = pin.PI6     # A03
GPIO_PI5 = PI5 = pin.PI5     # A04
SPI2_NSS = PI0 = pin.PI0     # A05
SPI2_SCK = PI1 = pin.PI1     # A06
FDCAN1_RX = PH14 = pin.PH14  # A07
FDCAN1_TX = PH13 = pin.PH13  # A08
I2C1_SCL = PH11 = pin.PH11   # A09
TIM12_CH2 = PH9 = pin.PH9    # A10
SPI4_MOSI = PE14 = pin.PE14  # A11
SPI4_NSS = PE11 = pin.PE11   # A12
GPIO_PH8 = PH8 = pin.PH8     # A13
GPIO_PD10 = PD10 = pin.PD10  # A14
GPIO_PH5 = PH5 = pin.PH5     # A15
USART2_RX = PF4 = pin.PF4    # A16
USART2_TX = PF5 = pin.PF5    # A17
I2C2_SCL = PF1 = pin.PF1     # A18
I2C2_SDA = PG15 = pin.PG15   # A19
GPIO_PD4 = PD4 = pin.PD4     # A20
GPIO_PD6 = PD6 = pin.PD6     # A21
I2C5_SDA = PD0 = pin.PD0     # A22
TIM4_CH2 = PB7 = pin.PB7     # A23
GPIO_PE3 = PE3 = pin.PE3     # A24
GPIO_PB15 = PB15 = pin.PB15  # A25
UART7_RX = PB3 = pin.PB3     # A26
GPIO_PE5 = PE5 = pin.PE5     # A27
GPIO_PB14 = PB14 = pin.PE14  # A28
# GND - VSS                    A29
# GND - VSS                    A30

# --------------------------------
# Header Location B
# --------------------------------
# VIN - VIN                    B01
ADC_IN1 = ANA1 = pin.PAN1    # B02
GPIO_PI7 = PI7 = pin.PI7     # B03
GPIO_PI4 = PI4 = pin.PI4     # B04
SPI2_MOSI = PI3 = pin.PI3    # B05
SPI2_MISO = PI2 = pin.PI2    # B06
GPIO_PH15 = PH15 = pin.PH15  # B07
I2C1_SDA = PH12 = pin.PH12   # B08
GPIO_PH10 = PH10 = pin.PH10  # B09
GPIO_PE15 = PE15 = pin.PE15  # B10
SPI4_SCK = PE12 = pin.PE12   # B11
GPIO_PH4 = PH4 = pin.PH4     # B12
SPI4_MISO = PE13 = pin.PE13  # B13
UART8_RX = PE0 = pin.PE0     # B14
UART8_TX = PE1 = pin.PE1     # B15
GPIO_PF0 = PF0 = pin.PF0     # B16
GPIO_PE6 = PE6 = pin.PE6     # B17
GPIO_PD7 = PD7 = pin.PD7     # B18
GPIO_PD5 = PD5 = pin.PD5     # B19
I2C5_SCL = PD1 = pin.PD1     # B20
GPIO_PD3 = PD3 = pin.PD3     # B21
TIM1_CH2 = PA9 = pin.PA9     # B22
GPIO_PB9 = PB9 = pin.PB9     # B23
GPIO_PB8 = PB8 = pin.PB8     # B24
GPIO_PB4 = PB4 = pin.PB4     # B25
GPIO_PG6 = PG6 = pin.PG6     # B26
UART7_TX = PA15 = pin.PA15   # B27
GPIO_PC7 = PC7 = pin.PC7     # B28
# USB1_DP - USB_DP1            B29
# USB1_DN - USB_DM1            B30

# --------------------------------
# Header Location C
# --------------------------------
# 3.3V - PMIC_V4OUT            C01
GPIO_PD9 = PD9 = pin.PD9     # C02
GPIO_PD15 = PD15 = pin.PD15  # C03
GPIO_PD14 = PD14 = pin.PD14  # C04
GPIO_PF3 = PF3 = pin.PF3     # C05
GPIO_PC3 = PC3 = pin.PC3     # C06
GPIO_PG13 = PG13 = pin.PG13  # C07
GPIO_PG1 = PG1 = pin.PG1     # C08
GPIO_PG4 = PG4 = pin.PG4     # C09
GPIO_PF14 = PF14 = pin.PF14  # C10
GPIO_PB1 = PB1 = pin.PB1     # C11
SPI6_MISO = PZ1 = pin.PZ1    # C12
SPI6_NSS = PZ3 = pin.PZ3     # C13
# PONKEY - PWC_PONKEY          C14
# VLD02 - PMIC_LD02            C15
# VBAT - VBAT                  C16
# VSW - PMC_SWOUT              C17
# VBST - PMIC_BSTOUT           C18
GPIO_PC5 = PC5 = pin.PC5     # C19
GPIO_PA1 = PA1 = pin.PA1     # C20
GPIO_PC4 = PC4 = pin.PC4     # C21
GPIO_PB10 = PB10 = pin.PB10  # C22
UART5_RX = PB12 = pin.PB12   # C23
GPIO_PC1 = PC1 = pin.PC1     # C24
GPIO_PA4 = PA4 = pin.PA4     # C25
GPIO_PA6 = PA6 = pin.PA6     # C26
GPIO_PD11 = PD11 = pin.PD11  # C27
GPIO_PF6 = PF6 = pin.PF6     # C28
GPIO_PD12 = PD12 = pin.PD12  # C29
GPIO_PB6 = PB6 = pin.PB6     # C30

# --------------------------------
# Header Location D
# --------------------------------
# 3.V - PMIC_V4OUT             D01
# RESETN - NRST                D02
GPIO_PD8 = PD8 = pin.PD8     # D03
GPIO_PA14 = PA14 = pin.PA14  # D04
GPIO_PG12 = PG12 = pin.PG12  # D05
GPIO_PA3 = PA3 = pin.PA3     # D06
GPIO_PE2 = PE2 = pin.PE2     # D07
GPIO_PG14 = PG14 = pin.PG14  # D08
GPIO_PG2 = PG2 = pin.PG2     # D09
GPIO_PB11 = PB11 = pin.PB11  # D10
GPIO_PF13 = PF13 = pin.PF13  # D11
SPI6_SCK = PZ0 = pin.PZ0     # D12
SPI6_MOSI = PZ2 = pin.PZ2    # D13
GPIO_PC2 = PC2 = pin.PC2     # D14
GPIO_PG0 = PG0 = pin.PG0     # D15
GPIO_PG3 = PG3 = pin.PG3     # D16
GPIO_PF15 = PF15 = pin.PF15  # D17
GPIO_PF12 = PF12 = pin.PF12  # D18
GPIO_PG5 = PG5 = pin.PG5     # D19
TIM3_CH2 = PB5 = pin.PB5     # D20
GPIO_PB0 = PB0 = pin.PB0     # D21
GPIO_PA7 = PA7 = pin.PA7     # D22
UART5_TX = PB13 = pin.PB13   # D23
GPIO_PA2 = PA2 = pin.PA2     # D24
GPIO_PA5 = PA5 = pin.PA5     # D25
GPIO_PC0 = PC0 = pin.PC0     # D26
GPIO_PF11 = PF11 = pin.PF11  # D27
GPIO_PD13 = PD13 = pin.PD13  # D28
# GND - VSS                    D29
# GND - VSS                    D30
# fmt: on

# I2C defaults
SDA1 = SDA = I2C1_SDA
SCL1 = SCL = I2C1_SCL
SDA2 = I2C2_SDA
SCL2 = I2C2_SCL
SDA5 = I2C5_SDA
SCL5 = I2C5_SCL

# SPI defaults
SCK = SPI2_SCK
MOSI = SPI2_MOSI
MISO = SPI2_MISO
CS = SPI2_NSS

# Board LED's
LED1_RED = pin.PZ6
LED1_GRN = pin.PZ7
LED2_RED = pin.PI8
LED2_GRN = pin.PI9

# Console UART
UART4_TX = pin.PG11
UART4_RX = pin.PB2
