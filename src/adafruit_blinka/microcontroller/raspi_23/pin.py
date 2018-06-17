# Pins dont exist in CPython so...lets make our own!
class Pin:
    def __init__(self, name, bcm_number):
        self._name = name
        self._number = bcm_number

SDA = Pin("SDA/D2", 2)
SCL = Pin("SCL/D3", 3)
D2 = Pin("SDA/D2", 2)
D3 = Pin("SCL/D3", 3)
D4 = Pin("BCM 4", 4)
D9 = Pin("MISO/D9", 9)
D10 = Pin("MOSI/D10", 10)
D11 = Pin("SCLK/D11", 11)
MISO = Pin("MISO/D9", 9)
MOSI = Pin("MOSI/D10", 10)
SCLK = Pin("SCLK/D11", 11)
D14 = Pin("TXD/D14", 14)
D15 = Pin("RXD/D15", 15)
TXD = Pin("TXD/D14", 14)
RXD = Pin("RXD/D15", 15)
D17 = Pin("BCM 17", 17)
D18 = Pin("BCM 18", 18)
D19 = Pin("BCM 19", 19)
D20 = Pin("BCM 20", 20)
MISO_2 = Pin("MISO_2/19", 19)
MOSI_2 = Pin("MOSI_2/20", 20)
SCLK_2 = Pin("SCLK_2/21", 21)
D21 = Pin("BCM 21", 21)
D22 = Pin("BCM 22", 22)
D23 = Pin("BCM 23", 23)
D24 = Pin("BCM 24", 24)
D27 = Pin("BCM 27", 27)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((1, SCLK, MOSI, MISO), (2, SCLK_2, MOSI_2, MISO_2))

# ordered as uartId, txId, rxId
uartPorts = (
    (1, TXD, RXD),
)

i2cPorts = (
    (1, SDA, SCL),
)

