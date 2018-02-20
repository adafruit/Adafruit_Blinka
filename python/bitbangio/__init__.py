from machine import I2C as _I2C
from machine import Pin

class I2C:
    def __init__(self, scl, sda, frequency=400000):
        self._locked = False
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

    def try_lock(self):
        if self._locked:
            return False
        else:
            self._locked=True
            return True

    def unlock(self):
        if self._locked:
            self._locked = False
        else:
            raise ValueError("Not locked")

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
