# ordered as spiId, sckId, mosiId, misoId
spiPorts = ((1, 14, 13, 12))

# ordered as uartId, txId, rxId
uartPorts = (
    (0, 1, 3),
    # (0, 15, 13) # TODO secondary pins for UART0 configurable from Micropython?
    (1, 2, None))
