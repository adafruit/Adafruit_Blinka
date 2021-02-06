"""Allwinner H616 Pin Names"""
from adafruit_blinka.microcontroller.generic_linux.libgpiod_pin import Pin

PC5  = Pin((1, 69))
PC6  = Pin((1, 70))
PC7 = Pin((1, 71))
PC8 = Pin((1, 72))
PC9 = Pin((1, 73))
PC10 = Pin((1, 74))
PC11 = Pin((1, 75))
PC14 = Pin((1, 78))
PC15 = Pin((1, 79))

PD14 = Pin((1, 110))
PD15 = Pin((1, 111))
PD16 = Pin((1, 112))
PD17 = Pin((1, 113))
PD18 = Pin((1, 114))
PD19 = Pin((1, 115))
UART2_TX = PD19
PD20 = Pin((1, 116))
UART2_RX = PD20
PD21 = Pin((1, 117))
PD22 = Pin((1, 118))
PD23 = Pin((1, 119))
PD24 = Pin((1, 120))
PD25 = Pin((1, 121))
TWI0_SCL = PD25
PD26 = Pin((1, 122))
TWI0_SDA = PD26

PG10 = Pin((1, 202))
PG11 = Pin((1, 203))
PG12 = Pin((1, 204))
PG13 = Pin((1, 205))
PG14 = Pin((1, 206))

PH2 = Pin((1, 226))
PH3 = Pin((1, 227))
PH4 = Pin((1, 228))
PH5 = Pin((1, 229))
PH6 = Pin((1, 230))
PH7 = Pin((1, 231))
PH8 = Pin((1, 232))
PH9 = Pin((1, 233))

PL8 = Pin((1, 360))
PL9 = Pin((1, 361))

i2cPorts = ((0, TWI0_SCL, TWI0_SDA),)
uartPorts = ((2, UART2_TX, UART2_RX),)
