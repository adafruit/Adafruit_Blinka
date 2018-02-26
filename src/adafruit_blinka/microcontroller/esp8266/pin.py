from microcontroller import Pin

GPIO0 = Pin(0)
GPIO1 = Pin(1)
GPIO2 = Pin(2)
GPIO3 = Pin(3)
GPIO4 = Pin(4)
GPIO5 = Pin(5)
GPIO12 = Pin(12)
GPIO13 = Pin(13)
GPIO14 = Pin(14)
GPIO15 = Pin(15)
GPIO16 = Pin(16)
TOUT = Pin("TOUT")
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

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((1, GPIO14, GPIO13, GPIO12))

# ordered as uartId, txId, rxId
uartPorts = (
    (0, GPIO1, GPIO3),
    # (0, GPIO15, GPIO13) # TODO secondary pins for UART0 configurable from Micropython? How to flag?
    (1, GPIO2, None))

i2cPorts = ()