class I2C:

    def __init__(self, *, frequency=400000):
        from adafruit_blinka.microcontroller.nova import Connection
        self._nova = Connection.getInstance()
        self._nova.setNumericalBase(10)
        self._nova.setOperationMode(0, "I2C")
        self._nova.setPullUpStateI2C(0, "EN")
        self._nova.setClockI2C(0, frequency)

    def scan(self):

        scanResults = []

        for i in range(8, 121):
            result = self._nova.scanAddrI2C(0, i<<1)

            resp = result.split(" ")

            if resp[3] == 'OK':
                scanResults.append(i)

        return scanResults

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):

        end = end if end else len(buffer)

        self._nova.startI2C(0, address<<1)

        for i in range(start, end): 
            self._nova.writeByteI2C(0, buffer[i])

        if stop:
            self._nova.endI2C(0)
        else:
            self._nova.endI2C(0, True)

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):

        end = end if end else len(buffer)

        result = self._nova.readBytesI2C(0, address<<1, len(buffer[start:end]))

        if result != "-NG":
            resp = result.split(" ")

            for i in range(len(buffer[start:end])):
                buffer[start+i] = int(resp[2+i])
        else:
            raise RuntimeError("Received error response from Binho Nova, result = " + result)

    def writeto_then_readfrom(self, address, buffer_out, buffer_in, *,
                              out_start=0, out_end=None,
                              in_start=0, in_end=None, stop=False):
    
        out_end = out_end if out_end else len(buffer_out)
        in_end = in_end if in_end else len(buffer_in)

        self._nova.startI2C(0, address<<1)

        for i in range(out_start, out_end): 
            self._nova.writeByteI2C(0, buffer_out[i])

        self._nova.endI2C(0, True)

        result = self._nova.readBytesI2C(0, address<<1, len(buffer_in[in_start:in_end]))

        if result != "-NG":
            resp = result.split(" ")

            for i in range(len(buffer_in[in_start:in_end])):
                buffer_in[in_start+i] = int(resp[2+i])
        else:
            raise RuntimeError("Received error response from Binho Nova, result = " + result)
