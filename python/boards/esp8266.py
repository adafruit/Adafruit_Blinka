# note GPIO0 and GPIO2 have built-in pull-ups on common ESP8266
# breakout boards making them suitable for I2C SDA and SCL

D0 = 16
D1 = 5
D2 = 4
D3 = 0
D4 = 2
D5 = 14
D6 = 12
D7 = 13
D8 = 15
D9 = 3
D10 = 1

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
