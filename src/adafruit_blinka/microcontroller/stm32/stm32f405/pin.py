"""STM32F405 pins"""

from microcontroller import Pin

A0 = Pin("A0")
A1 = Pin("A1")
A2 = Pin("A2")
A3 = Pin("A3")
A4 = Pin("A4")
A5 = Pin("A5")
A6 = Pin("A6")
A7 = Pin("A7")
A8 = Pin("A8")
A9 = Pin("A9")
A10 = Pin("A10")
A11 = Pin("A11")
A12 = Pin("A12")
A13 = Pin("A13")
A14 = Pin("A14")
A15 = Pin("A15")
B0 = Pin("B0")
B1 = Pin("B1")
B2 = Pin("B2")
B3 = Pin("B3")
B4 = Pin("B4")
B5 = Pin("B5")
B6 = Pin("B6")
B7 = Pin("B7")
B8 = Pin("B8")
B9 = Pin("B9")
B10 = Pin("B10")
B11 = Pin("B11")
B12 = Pin("B12")
B13 = Pin("B13")
B14 = Pin("B14")
B15 = Pin("B15")
C0 = Pin("C0")
C1 = Pin("C1")
C2 = Pin("C2")
C3 = Pin("C3")
C4 = Pin("C4")
C5 = Pin("C5")
C6 = Pin("C6")
C7 = Pin("C7")
C8 = Pin("C8")
C9 = Pin("C9")
C10 = Pin("C10")
C11 = Pin("C11")
C12 = Pin("C12")
C13 = Pin("C13")
D2 = Pin("D2")

# ordered as spiId, sckId, mosiId, misoId
SPI_PORTS = ((1, B13, B15, B14), (2, A5, A6, A7))

# ordered as uartId, txId, rxId
UART_PORTS = (
    (1, B6, B7),
    (2, A2, A3),
    (3, B10, B11),
    (4, A0, A1),
    (6, C6, C7),
)

I2C_PORTS = (
    (1, B6, B7),
    (2, B10, B11),
)
