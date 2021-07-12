"""UART Class for RP2040"""
from machine import UART as _UART
from machine import Pin
from microcontroller.pin import uartPorts

# pylint: disable=protected-access, no-self-use
class UART:
    """Custom UART Class for RP2040"""

    # pylint: disable=too-many-arguments
    def __init__(self, tx, rx, baudrate=9600, bits=8, parity=None, stop=1):
        # check tx and rx have hardware support
        for portId, txPin, rxPin in uartPorts:
            if txPin == tx and rxPin == rx:
                self._uart = _UART(
                    portId,
                    baudrate,
                    bits=bits,
                    parity=parity,
                    stop=stop,
                    tx=Pin(txPin.id),
                    rx=Pin(rxPin.id),
                )
                break
        else:
            raise ValueError(
                "No Hardware UART on (tx,rx)={}\nValid UART ports: {}".format(
                    (tx.id, rx.id), uartPorts
                )
            )

    # pylint: enable=too-many-arguments

    def read(self, nbytes=None):
        """Read from the UART"""
        return self._uart.read(nbytes)

    def readinto(self, buf, nbytes=None):
        """Read from the UART into a buffer"""
        return self._uart.readinto(buf, nbytes)

    def readline(self):
        """Read a line of characters up to a newline charater from the UART"""
        return self._uart.readline()

    def write(self, buf):
        """Write to the UART from a buffer"""
        return self._uart.write(buf)
