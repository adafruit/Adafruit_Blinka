import spidev
import time
from adafruit_blinka.agnostic import detector

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
            mode |= self.CPOL
        if phase:
            mode |= self.CPHA

        self.clock_pin = sck
        self.mosi_pin = mosi
        self.miso_pin = miso
        self.baudrate = baudrate
        self.mode = mode
        self.bits = bits
        self.chip = detector.chip

    def set_no_cs(self):
        # Linux SPI driver for AM33XX chip in BeagleBone and PocketBeagle
        # does not support setting SPI_NO_CS mode bit (issue #104)
        if not self.chip.AM33XX and not self.chip.IMX8MX:
            try:
                self._spi.no_cs = True  # this doesn't work but try anyways
            except AttributeError:
                pass

    def write(self, buf, start=0, end=None):
        if not buf:
            return
        if end is None:
            end = len(buf)
        try:
            self._spi.open(self._port, 0)
            self.set_no_cs()
            self._spi.max_speed_hz = self.baudrate
            self._spi.mode = self.mode
            self._spi.bits_per_word = self.bits
            self._spi.writebytes([x for x in buf[start:end]])
            self._spi.close()
        except FileNotFoundError as not_found:
            print("Could not open SPI device - check if SPI is enabled in kernel!")
            raise

    def readinto(self, buf, start=0, end=None, write_value=0):
        if not buf:
            return
        if end is None:
            end = len(buf)
        try:
            self._spi.open(self._port, 0)
            self.set_no_cs()
            self._spi.max_speed_hz = self.baudrate
            self._spi.mode = self.mode
            self._spi.bits_per_word = self.bits
            data = self._spi.xfer([write_value]*(end-start))
            for i in range(end-start):  # 'readinto' the given buffer
              buf[start+i] = data[i]
            self._spi.close()
        except FileNotFoundError as not_found:
            print("Could not open SPI device - check if SPI is enabled in kernel!")
            raise

    def write_readinto(self, buffer_out, buffer_in, out_start=0,
                       out_end=None, in_start=0, in_end=None):
        if not buffer_out or not buffer_in:
            return
        if out_end is None:
            out_end = len(buffer_out)
        if in_end is None:
            in_end = len(buffer_in)
        if out_end - out_start != in_end - in_start:
            raise RuntimeError('Buffer slices must be of equal length.')
        try:
            self._spi.open(self._port, 0)
            self.set_no_cs()
            self._spi.max_speed_hz = self.baudrate
            self._spi.mode = self.mode
            self._spi.bits_per_word = self.bits
            data = self._spi.xfer(list(buffer_out[out_start:out_end+1]))
            for i in range((in_end - in_start)):
                buffer_in[i+in_start] = data[i]
            self._spi.close()
        except FileNotFoundError as not_found:
            print("Could not open SPI device - check if SPI is enabled in kernel!")
            raise
