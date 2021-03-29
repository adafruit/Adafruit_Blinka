"""Pin definitions for the LubanCat IMX6ULL."""

from adafruit_blinka.microcontroller.nxp_imx6ull import pin

# Pro board pin header CN4 named GPIO_PAx, pin header CN5 named GPIO_PBx
# Mini board pin header CN3 named GPIO_PCx, pin header CN4 named GPIO_PDx

# Board pin name [= alias] = RPI name [= alias] = pin name
GPIO_PC3 = I2C2_SDA = D2 = SDA = pin.I2C2_SDA
GPIO_PC5 = I2C2_SCL = D3 = SCL = pin.I2C2_SCL

GPIO_PC7 = D4 = pin.GPIO27
GPIO_PC8 = D14 = TXD = pin.UART3_TXD
GPIO_PC10 = D15 = RXD = pin.UART3_RXD
GPIO_PC11 = ADC_IN3 = A3 = D17 = pin.GPIO3
GPIO_PC12 = D18 = pin.GPIO112
GPIO_PC13 = ADC_IN2 = A2 = D27 = pin.GPIO2
GPIO_PC15 = ADC_IN0 = A0 = D22 = pin.GPIO0
GPIO_PC16 = D23 = pin.GPIO119
GPIO_PC18 = D24 = pin.GPIO114

GPIO_PC19 = ECSPI3_MOSI = D10 = MOSI = pin.ECSPI3_MOSI
GPIO_PC21 = ECSPI3_MISO = D9 = MISO = pin.ECSPI3_MISO
GPIO_PC22 = D25 = pin.GPIO27
GPIO_PC23 = ECSPI3_SCLK = D11 = SCLK = SCK = pin.ECSPI3_SCLK
GPIO_PC24 = ECSPI3_SS0 = D8 = SS0 = pin.ECSPI3_SS0
GPIO_PC26 = ECSPI3_SS1 = D7 = SS1 = pin.ECSPI3_SS1

GPIO_PC27 = I2C3_SDA = D0 = pin.I2C3_SDA
GPIO_PC28 = I2C3_SCL = D1 = pin.I2C3_SCL

GPIO_PC29 = D5 = pin.GPIO117
GPIO_PC31 = D6 = pin.GPIO118

GPIO_PC32 = LED_D6 = D12 = pin.GPIO115
GPIO_PC33 = LED_D5 = D13 = pin.GPIO116

# Board pwm channel = RPI PWM Channel = pin name
PWM_C7 = PWM1 = pin.GPIO115
PWM_C8 = PWM2 = pin.GPIO116

GPIO_PC35 = D19 = pin.GPIO121
GPIO_PC36 = D16 = pin.GPIO120
GPIO_PC37 = D26 = pin.GPIO26
GPIO_PC38 = D20 = pin.GPIO123
GPIO_PC40 = D21 = pin.GPIO124

# Mini header CN4
GPIO_PD9 = ADC_IN1 = A1 = pin.GPIO1
GPIO_PD4 = LED_D4 = PWM_C3 = pin.GPIO4
GPIO_PD17 = BUTTON2 = pin.GPIO129
