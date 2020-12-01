"""Pin definitions for the Odroid C4."""

from adafruit_blinka.microcontroller.amlogic.s905x3 import pin

for it in pin.i2cPorts:
    globals()["SCL" + str(it[0])] = it[1]
    globals()["SDA" + str(it[0])] = it[2]

SCL = pin.i2cPorts[0][1]
SDA = pin.i2cPorts[0][2]

SCLK = pin.SPI0_SCLK
MOSI = pin.SPI0_MOSI
MISO = pin.SPI0_MISO
SPI_CS0 = pin.SPI0_CS0

"""J2: physical pin number"""

D3 = pin.GPIOX_17
D5 = pin.GPIOX_18
D7 = pin.GPIOX_5
D8 = pin.GPIOX_12
D10 = pin.GPIOX_13
D11 = pin.GPIOX_3
D12 = pin.GPIOX_16
D13 = pin.GPIOX_4
D15 = pin.GPIOX_7
D16 = pin.GPIOX_0
D18 = pin.GPIOX_1
D19 = pin.GPIOX_8
D21 = pin.GPIOX_9
D22 = pin.GPIOX_2
D23 = pin.GPIOX_11
D24 = pin.GPIOX_10
D26 = pin.GPIOH_6
D27 = pin.GPIOA_14
D28 = pin.GPIOA_15
D29 = pin.GPIOX_14
D31 = pin.GPIOX_15
D32 = pin.GPIOH_7
D33 = pin.GPIOX_6
D35 = pin.GPIOX_19
D36 = pin.GPIOH_5

"""J7: physical pin number"""

D42 = pin.GPIOAO_10
D44 = pin.GPIOAO_9
D45 = pin.GPIOAO_7
D46 = pin.GPIOAO_8
D47 = pin.GPIOAO_4
