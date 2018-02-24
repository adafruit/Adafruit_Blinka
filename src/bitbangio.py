from adafruit_blinka import Lockable
from machine import I2C as _I2C
from machine import Pin


class I2C(Lockable):
    def __init__(self, scl, sda, frequency=400000):
        super().__init()
        self.init(scl, sda, frequency)

    def init(self, scl, sda, frequency):
        self.deinit()
        id = -1 # force bitbanging implementation - in future introspect platform if SDA/SCL matches hardware I2C
        self._i2c = _I2C(id, Pin(scl.id), Pin(sda.id), freq=frequency)

    def deinit(self):
        try:
            del self._i2c
        except AttributeError:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()

    def scan(self):
        return self._i2c.scan()

    def readfrom_into(self, address, buffer, start=0, end=None):
        if start is not 0 or end is not None:
            if end is None:
                end = len(buffer)
            buffer = memoryview(buffer)[start:end]
        stop = True # remove for efficiency later
        return self._i2c.readfrom_into(address, buffer, stop)

    def writeto(self, address, buffer, start=0, end=None, stop=True, *a, **k):
        if start is not 0 or end is not None:
            if end is None:
                end = len(buffer)
            buffer = memoryview(buffer)[start:end]
        return self._i2c.writeto(address, buffer, stop)

# TODO untested, as actually busio.SPI was on tasklist https://github.com/adafruit/Adafruit_Micropython_Blinka/issues/2 :(
class SPI(Lockable):
    def __init__(self, clock, MOSI=None, MISO=None):
        self._spi = SPI(-1)
        self._pins = (clock.id, MOSI.id, MISO.id)

    def configure(self, baudrate=100000, polarity=0, phase=0, bits=8):
        if self._locked:
            # TODO verify if _spi obj 'caches' sck, mosi, miso to avoid storing in _attributeIds (duplicated in busio)
            # i.e. #init ignores MOSI=None rather than unsetting
            self._spi.init(baudrate=baudrate, polarity=polarity, phase=phase, bits = bits, firstbit = SPI.MSB, sck = Pin(self._pins[0]), mosi=Pin(self._pins[1]), miso=Pin(self._pins[2]))
        else:
            raise RuntimeError("First call try_lock()")

    def write(self, buf):
        return self._spi.write(buf)

    def readinto(self, buf):
        return self.readinto(buf)

    def write_readinto(self, buffer_out, buffer_in):
        return self.write_readinto(buffer_out, buffer_in)
