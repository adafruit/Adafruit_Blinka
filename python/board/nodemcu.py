from microcontroller.pin import *
# note GPIO0 and GPIO2 have built-in pull-ups on common ESP8266
# breakout boards making them suitable for I2C SDA and SCL

D0 = GPIO16
D1 = GPIO5
D2 = GPIO4
D3 = GPIO0
D4 = GPIO2
D5 = GPIO14
D6 = GPIO12
D7 = GPIO13
D8 = GPIO15
D9 = GPIO3
D10 = GPIO1

TX1 = D4
"""Transmit pin from second (transmit-only) UART """

CLK = D5
"""SPI clock pin"""
MISO = D6
"""SPI MISO (Master in, Slave out)"""
MOSI = D7
"""SPI MOSI (Master out, Slave in)"""

RX0 = D9
TX0 = D10
