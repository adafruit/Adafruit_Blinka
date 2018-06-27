"""NodeMCU pin names"""

from adafruit_blinka.microcontroller.esp8266 import pin

D0 = pin.GPIO16
D1 = pin.GPIO5
D2 = pin.GPIO4
D3 = pin.GPIO0
D4 = pin.GPIO2
D5 = pin.GPIO14
D6 = pin.GPIO12
D7 = pin.GPIO13
D8 = pin.GPIO15
D9 = pin.GPIO3
D10 = pin.GPIO1

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

# GPIO0 and GPIO2 have built-in pull-ups on common ESP8266
# breakout boards making them suitable for I2C SDA and SCL
