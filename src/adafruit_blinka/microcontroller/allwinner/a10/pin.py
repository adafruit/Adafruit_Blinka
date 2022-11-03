"""Allwinner A10 pin names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PB2 = Pin(34) # PB2/PWM0
PWM0 = PB2
PB20 = Pin(52) # PB20/TWI2_SDL
TWI2_SCL = PB20
PB21 = Pin(53) # PB20/TWI2_SDA
TWI2_SDA = PB21

PC19 = Pin(83) # PC19/SPI2_CS
SPI2_CS = PC19
PC20 = Pin(84) # PC20/SPI2_SCLK
SPI2_SCLK = PC20
PC21 = Pin(85) # PC21/SPI2_MOSI
SPI2_MOSI = PC21
PC22 = Pin(86) # PC22/SPI2_MISO
SPI2_MISO = PC22

PH5 = Pin(229)
PH6 = Pin(230) # PH6/UART5_TX
UART5_TX = PH6
PH7 = Pin(231) # PH7/UART5_RX
UART5_RX = PH7
PH8 = Pin(232)
PH9 = Pin(233)
PH10 = Pin(234)
PH11 = Pin(235)
PH12 = Pin(236)
PH13 = Pin(237)
PH14 = Pin(238)
PH15 = Pin(239)
PH16 = Pin(240)
PH17 = Pin(241)
PH18 = Pin(242)
PH19 = Pin(243)

PI3 = Pin(259) # PI3/PWM1
PWM1 = PI3
PI10 = Pin(266) # PI10/SPI0_CS/UART5_TX
SPI0_CS = PI10
PI11 = Pin(267) # PI11/SPI0_SCLK/UART5_RX
SPI0_SCLK = PI11
PI12 = Pin(268)
SPI0_MOSI = PI12
UART6_TX = PI12
PI13 = Pin(269)
SPI0_MISO = PI13
UART6_RX = PI13
PI18 = Pin(274) # PI18/UART2_TX
UART2_TX = PI18
PI19 = Pin(275) # PI19/UART2_RX
UART2_RX = PI19

XP_TP = 1 # Allwinner touch panel controller which can be configured to operate
XN_TP = 2 # as four seperate adc chanels, providing 12-bit resolution.
YP_TP = 3
YN_TP = 4

# Ordered as i2cId, SCL, SDA
i2cPorts =((2, TWI2_SCL, TWI2_SDA),)

# Ordered as spiId, clkId, mosiId, misoId
spiPorts =((0, SPI0_SCLK, SPI0_MOSI, SPI0_MISO),
           (2, SPI2_SCLK, SPI2_MOSI, SPI2_MISO),
)

# ordered as uartId, txId, rxId
uartPorts = (
    (2, UART2_TX, UART2_RX),
    (5, UART5_TX, UART5_RX),
    (6, UART6_TX, UART6_RX),
)
# sysFs pwm outputs, pwm channel and pin first tuple
pwmOuts = (((0,0), PWM0),
           ((0,1), PWM1),
)

#sysFs analog inputs, Ordered as analogInId, device, and channel
analogIns = ((XP_TP, 0, 0),
             (XN_TP, 0, 1),
             (YP_TP, 0, 2),
             (YN_TP, 0, 3),
)
