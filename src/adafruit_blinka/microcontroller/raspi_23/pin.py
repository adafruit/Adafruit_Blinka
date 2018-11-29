try:
    # Start by seeing if we can support the libgpiod-based generic linux driver:
    from adafruit_blinka.microcontroller.generic_linux.pin import Pin
except ImportError:
    # Failing that, fall back to the RPi.GPIO-based version:
    from adafruit_blinka.microcontroller.raspi_23.pin_rpi_gpio import Pin

D2 = Pin(2)
SDA = Pin(2)
D3 = Pin(3)
SCL = Pin(3)

D4 = Pin(4)
D5 = Pin(5)
D6 = Pin(6)

D7 = Pin(7)
CE1 = Pin(7)
D8 = Pin(8)
CE0 = Pin(8)
D9 = Pin(9)
MISO = Pin(9)
D10 = Pin(10)
MOSI = Pin(10)
D11 = Pin(11)
SCLK = Pin(11) # Raspberry Pi naming
SCK = Pin(11)  # CircuitPython naming

D12 = Pin(12)
D13 = Pin(13)

D14 = Pin(14)
TXD = Pin(14)
D15 = Pin(15)
RXD = Pin(15)

D16 = Pin(16)
D17 = Pin(17)
D18 = Pin(18)
D19 = Pin(19)
MISO_1 = Pin(19)
D20 = Pin(20)
MOSI_1 = Pin(20)
D21 = Pin(21)
SCLK_1 = Pin(21)
SCK_1 = Pin(21)
D22 = Pin(22)
D23 = Pin(23)
D24 = Pin(24)
D25 = Pin(25)
D26 = Pin(26)
D27 = Pin(27)

# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((0, SCLK, MOSI, MISO), (1, SCLK_1, MOSI_1, MISO_1))

# ordered as uartId, txId, rxId
uartPorts = (
    (1, TXD, RXD),
)

i2cPorts = (
    (1, SCL, SDA),
)
