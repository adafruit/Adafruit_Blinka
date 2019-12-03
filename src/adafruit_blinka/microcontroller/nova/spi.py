class SPI:
    MSB = 0
    PAYLOAD_MAX_LENGTH = 64

    def __init__(self, clock):
        from adafruit_blinka.microcontroller.nova import Connection
        self._nova = Connection.getInstance()
        self._nova.setNumericalBase(10)
        self._nova.setOperationMode(0, 'SPI')
        self._nova.setClockSPI(0, clock)
        self._nova.setModeSPI(0, 0)
        self._nova.setIOpinMode(0, 'DOUT')
        self._nova.setIOpinMode(1, 'DOUT')
        self._nova.beginSPI(0)

        # Cpol and Cpha set by mode
        # Mode  Cpol Cpha
        #  0     0    0
        #  1     0    1
        #  2     1    0
        #  3     1    1

    def init(self, baudrate=100000, polarity=0, phase=0, bits=8,
             firstbit=MSB, sck=None, mosi=None, miso=None):
        #print("baudrate: " + str(baudrate))
        #print("mode: " + str((polarity<<1) | (phase)))
        self._nova.setClockSPI(0, baudrate)
        self._nova.setModeSPI(0, (polarity<<1) | (phase))

    @staticmethod
    def get_received_data(lineOutput):
        return (lineOutput.split('RXD ')[1])

    @property
    def frequency(self):
        return self._nova.getClockSPI(0).split('CLK ')[1]

    def write(self, buf, start=0, end=None):
        end = end if end else len(buf)
        chunks, rest = divmod(end - start, self.PAYLOAD_MAX_LENGTH)
        for i in range(chunks):
            chunk_start = start + i * self.PAYLOAD_MAX_LENGTH
            chunk_end = chunk_start + self.PAYLOAD_MAX_LENGTH
            buffer_data = buf[chunk_start:chunk_end]
            self._nova.clearBuffer(0)
            self._nova.writeToBuffer(0, 0, buffer_data)
            self._nova.transferBufferSPI(0, chunk_end - chunk_start + 1)
        if rest:
            buffer_data = buf[-1*rest:]
            self._nova.clearBuffer(0)
            self._nova.writeToBuffer(0, 0, buffer_data)
            self._nova.transferBufferSPI(0, rest)

    def readinto(self, buf, start=0, end=None, write_value=0):
        end = end if end else len(buf)
        for i in range(start, end):
            buf[start+i] = int(self.get_received_data(self._nova.transferSPI(0, write_value)))

    def write_readinto(self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None):
        out_end = out_end if out_end else len(buffer_out)
        in_end = in_end if in_end else len(buffer_in)
        readlen = in_end-in_start
        writelen = out_end-out_start
        if readlen > writelen:
            # resize out and pad with 0's
            tmp = bytearray(buffer_out)
            tmp.extend([0] * (readlen - len(buffer_out)))
            buffer_out = tmp
        i = 0
        for data_out in buffer_out:
            data_in = int(self.get_received_data(self._nova.transferSPI(0, data_out)))
            if i < readlen:
                buffer_in[in_start+i] = data_in
            i += 1
