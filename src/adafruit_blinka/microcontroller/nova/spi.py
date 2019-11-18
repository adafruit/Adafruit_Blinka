#from adafruit_blinka.microcontroller.nova.pin import Pin

class SPI:
    MSB = 0

    def __init__(self, clock):
        from binhoHostAdapter import binhoHostAdapter
        from binhoHostAdapter import binhoUtilities

        utilities = binhoUtilities.binhoUtilities()
        devices = utilities.listAvailableDevices()

        if len(devices) > 0:
            self._nova = binhoHostAdapter.binhoHostAdapter(devices[0])
            self._nova.setOperationMode(0, 'SPI')
            self._nova.setClockSPI(0, clock)
            self._nova.setModeSPI(0, 0)
            self._nova.setIOpinMode(0, 'DOUT')
            self._nova.setIOpinValue(0, 'HIGH')
            self._nova.beginSPI(0)
            # Cpol and Cpha set by mode
            # Mode  Cpol Cpha
            #  0     0    0
            #  1     0    1
            #  2     1    0
            #  3     1    1

        else:
            raise RuntimeError('No Binho host adapter found!')

    def init(self, baudrate=100000, polarity=0, phase=0, bits=8,
                  firstbit=MSB, sck=None, mosi=None, miso=None):
        print("baudrate: " + baudrate)
        print("mode: " + (polarity<<1) | (phase))
        self._nova.setClockSPI(0, baudrate)
        self._nova.setModeSPI(0, (polarity<<1) | (phase))

    @staticmethod
    def getSpiReceivedData(lineOutput):
        return (lineOutput.split('RXD ')[1])

    @property
    def frequency(self):
        return self._nova.getClockSPI(0)

    def write(self, buf, start=0, end=None):
        end = end if end else len(buf)
        #chunks, rest = divmod(end - start, self._spi.PAYLOAD_MAX_LENGTH)
        #for i in range(chunks):
        #    chunk_start = start + i * self._spi.PAYLOAD_MAX_LENGTH
        #    chunk_end = chunk_start + self._spi.PAYLOAD_MAX_LENGTH
        #    self._port.write(buf[chunk_start:chunk_end])
        #if rest:
        #    self._port.write(buf[-1*rest:])

    def readinto(self, buf, start=0, end=None, write_value=0):
        end = end if end else len(buf)
        self._nova.setIOpinValue(0, 'LOW')
        for i in range(start, end):
            buf[start+i] = int(self.getSpiReceivedData(self._nova.transferSPI(0, write_value)), 16)
        self._nova.setIOpinValue(0, 'HIGH')
"""
    def write_readinto(self, buffer_out, buffer_in,  out_start=0, out_end=None, in_start=0, in_end=None):
        out_end = out_end if out_end else len(buffer_out)
        in_end = in_end if in_end else len(buffer_in)
        result = self._port.exchange(buffer_out[out_start:out_end],
                                     in_end-in_start, duplex=True)
        for i, b in enumerate(result):
            buffer_in[in_start+i] = b
"""