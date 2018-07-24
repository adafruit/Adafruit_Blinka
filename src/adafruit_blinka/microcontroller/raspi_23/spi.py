import spidev
import time

class SPI:
    MSB = 0
    LSB = 1
    CPHA = 1
    CPOL = 2

    baudrate = 100000
    mode = 0
    bits = 8

    def __init__(self, portid):
        self._port = portid
        self._spi = spidev.SpiDev()

    def init(self, baudrate=100000, polarity=0, phase=0, bits=8,
                  firstbit=MSB, sck=None, mosi=None, miso=None):
        mode = 0
        if polarity:
            mode |= CPOL
        if phase:
            mode |= CPHA

        self.clock_pin = sck
        self.mosi_pin = mosi
        self.miso_pin = miso
        self.baudrate = baudrate
        self.mode = mode
        self.bits = bits

    def write(self, buf):
        if not buf:
            return
        try:
            self._spi.open(self._port, 0)
            try:
              self._spi.no_cs = True  # this doesn't work but try anyways
            except AttributeError:
              pass
            self._spi.max_speed_hz = self.baudrate
            self._spi.mode = self.mode
            self._spi.bits_per_word = self.bits
            self._spi.writebytes([x for x in buf])
            self._spi.close()
        except FileNotFoundError as not_found:
            print("Could not open SPI device - check if SPI is enabled in kernel!")
            raise

    def readinto(self, buf):
        if not buf:
            return
        try:
            self._spi.open(self._port, 0)
            try:
              self._spi.no_cs = True  # this doesn't work but try anyways
            except AttributeError:
              pass
            self._spi.max_speed_hz = self.baudrate
            self._spi.mode = self.mode
            self._spi.bits_per_word = self.bits
            data = self._spi.readbytes(len(buf))
            for i in range(len(buf)):  # 'readinto' the given buffer
              buf[i] = data[i]
            self._spi.close()
        except FileNotFoundError as not_found:
            print("Could not open SPI device - check if SPI is enabled in kernel!")
            raise

    def write_readinto(self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None):
        if not buffer_out or not buffer_in:
            return
        if out_end - out_start != in_end - in_start:
            raise RuntimeError
        try:
            self._spi.open(self._port, 0)
            try:
                self._spi.no_cs = True  # this doesn't work but try anyways
            except AttributeError:
                pass
            self._spi.max_speed_hz = self.baudrate
            self._spi.mode = self.mode
            self._spi.bits_per_word = self.bits
            data = self._spi.xfer(list(buffer_out))
            for i in range(len(buffer_in)): # 'readinto' the given buffer
                buffer_in[i] = data[i]
            self._spi.close()
        except FileNotFoundError as not_found:
            print("Could not open SPI device - check if SPI is enabled in kernel!")
            raise