"""UART Class for Binho Nova"""

from adafruit_blinka.microcontroller.nova import Connection


class UART:
    """Custom UART Class for Binho Nova"""

    ESCAPE_SEQUENCE = "+++UART0"

    # pylint: disable=too-many-arguments,unused-argument
    def __init__(
        self,
        portid,
        baudrate=9600,
        bits=8,
        parity=None,
        stop=1,
        timeout=1000,
        read_buf_len=None,
        flow=None,
    ):
        self._nova = Connection.getInstance()

        self._id = portid
        self._baudrate = baudrate
        self._parity = parity
        self._bits = bits
        self._stop = stop
        self._timeout = timeout

        if flow is not None:  # default 0
            raise NotImplementedError(
                "Parameter '{}' unsupported on Binho Nova".format("flow")
            )

        self._nova.setOperationMode(self._id, "UART")
        self._nova.setBaudRateUART(self._id, baudrate)
        self._nova.setDataBitsUART(self._id, bits)
        self._nova.setParityUART(self._id, parity)
        self._nova.setStopBitsUART(self._id, stop)
        self._nova.setEscapeSequenceUART(self._id, UART.ESCAPE_SEQUENCE)
        self._nova.beginBridgeUART(self._id)

    # pylint: enable=too-many-arguments,unused-argument
    def __del__(self):
        """Close Nova on delete"""
        self.deinit()
        self._nova.close()

    def deinit(self):
        """Deinitialize"""
        self._nova.writeBridgeUART(UART.ESCAPE_SEQUENCE)
        self._nova.stopBridgeUART(UART.ESCAPE_SEQUENCE)

    def read(self, nbytes=None):
        """Read data from UART and return it"""
        if nbytes is None:
            return None
        data = bytearray()
        for _ in range(nbytes):
            data.append(ord(self._nova.readBridgeUART()))
        return data

    def readinto(self, buf, nbytes=None):
        """Read data from UART and into the buffer"""
        if nbytes is None:
            return None
        for _ in range(nbytes):
            buf.append(ord(self._nova.readBridgeUART()))
        return buf

    def readline(self):
        """Read a single line of data from UART"""
        out = self._nova.readBridgeUART()
        line = out
        while out != "\r":
            out = self._nova.readBridgeUART()
            line += out
        return line

    def write(self, buf):
        """Write data from the buffer to UART"""
        return self._nova.writeBridgeUART(buf)
