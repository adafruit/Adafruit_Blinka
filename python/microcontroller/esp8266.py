from microcontroller import Pin as pin

pin.GPIO0=pin(0)
pin.GPIO1=pin(1)
pin.GPIO2=pin(2)
pin.GPIO3=pin(3)
pin.GPIO4=pin(4)
pin.GPIO5=pin(5)
pin.GPIO12=pin(12)
pin.GPIO13=pin(13)
pin.GPIO14=pin(14)
pin.GPIO15=pin(15)
pin.GPIO16=pin(16)
pin.TOUT=pin("TOUT")

"""
From introspection of microcontroller.pin on Feather Huzzah running CircuitPython
>>> dir(microcontroller.pin)
['TOUT', 'XPD_DCDC', 'MTMS', 'MTDI', 'MTCK', 'MTDO', 'GPIO2', 'GPIO0', 'GPIO4', 'SD_DATA_2', 'SD_DATA_3', 'SD_CMD', 'SD_CLK', 'SD_DATA_0', 'SD_DATA_1', 'DVDD', 'U0RXD', 'U0TXD']
>>> dir(board)
['ADC', 'GPIO16', 'GPIO14', 'SCK', 'GPIO12', 'MISO', 'GPIO13', 'MOSI', 'GPIO15', 'GPIO2', 'GPIO0', 'GPIO4', 'SDA', 'RX', 'TX', 'GPIO5', 'SCL']
"""

"""
class cpu():
    def frequency(self):
        from machine import freq
        return freq()
"""
