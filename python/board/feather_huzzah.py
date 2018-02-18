from microcontroller.esp8266 import pin

GPIO0=pin.GPIO0
GPIO1=pin.GPIO1
GPIO2=pin.GPIO2
GPIO3=pin.GPIO3
GPIO4=pin.GPIO4
GPIO5=pin.GPIO5
GPIO12=pin.GPIO12
GPIO13=pin.GPIO13
GPIO14=pin.GPIO14
GPIO15=pin.GPIO15
GPIO16=pin.GPIO16

ADC=pin.TOUT

MISO=GPIO12
MOSI=GPIO13
SCK=GPIO14

RX=GPIO3
TX=GPIO1

# GPIO0 and GPIO2 have built-in pull-ups on common ESP8266
# breakout boards making them suitable for I2C SDA and SCL
SDA=GPIO0
SCL=GPIO2




['ADC', 'GPIO16', 'GPIO14', 'SCK', 'GPIO12', 'MISO', 'GPIO13', 'MOSI', 'GPIO15', 'GPIO2', 'GPIO0', 'GPIO4', 'SDA', 'RX', 'TX', 'GPIO5', 'SCL']
