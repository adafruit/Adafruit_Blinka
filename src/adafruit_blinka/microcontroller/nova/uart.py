import time

class UART():
    ESCAPE_SEQUENCE = "+++UART0"
    def __init__(self,
                 portid,
                 baudrate=9600,
                 bits=8,
                 parity=None,
                 stop=1,
                 timeout=1000,
                 read_buf_len=None,
                 flow=None):
        from adafruit_blinka.microcontroller.nova import Connection
        self._nova = Connection.getInstance()

        self._id = portid
        self._baudrate = baudrate
        self._parity = parity
        self._bits = bits
        self._stop = stop
        self._timeout = timeout

        if flow is not None:  # default 0
            raise NotImplementedError(
                "Parameter '{}' unsupported on Binho Nova".format(
                    "flow"))

        self._nova.setOperationMode(self._id, 'UART')
        self._nova.setBaudRateUART(self._id, baudrate)
        self._nova.setDataBitsUART(self._id, bits)
        self._nova.setParityUART(self._id, parity)
        self._nova.setStopBitsUART(self._id, stop)
        self._nova.setEscapeSequenceUART(self._id, UART.ESCAPE_SEQUENCE)
        self._nova.beginBridgeUART(self._id)

    def deinit(self):
        self._nova.writeBridgeUART(UART.ESCAPE_SEQUENCE)
        self._nova.stopBridgeUART(UART.ESCAPE_SEQUENCE)

    def read(self, nbytes=None):
        if nbytes is None:
            return None
        data = bytearray()
        for i in range(nbytes):
            data.append(ord(self._nova.readBridgeUART()))
        return data

    def readinto(self, buf, nbytes=None):
        if nbytes is None:
            return None
        for i in range(nbytes):
            buf.append(ord(self._nova.readBridgeUART()))
        return buf

    def readline(self):
        out = self._nova.readBridgeUART()
        line = out
        while out != '\r':
            out = self._nova.readBridgeUART()
            line += out
        return line

    def write(self, buf):
        return self._nova.writeBridgeUART(buf)
