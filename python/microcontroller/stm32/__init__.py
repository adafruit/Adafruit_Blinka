from microcontroller import pin

# ordered as spiId, sckId, mosiId, misoId
spiPorts = (
    (1, "B13", "B15", "B14"),
    (2, "A5", "A6", "A7")
)

# ordered as uartId, txId, rxId
uartPorts = (
    (1, "B6", "B7"),
    (2, "A2", "A3"),
    (3, "B10", "B11"),
    (4, "A0", "A1"),
    (6, "C6", "C7"),
)