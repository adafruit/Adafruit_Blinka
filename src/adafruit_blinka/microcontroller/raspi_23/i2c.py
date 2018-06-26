import Adafruit_PureIO.smbus as smbus
import time

class I2C:
    MASTER = 0
    SLAVE = 1
    _baudrate = None
    _mode = None
    _i2c_bus = None

    def __init__(self, bus_num, mode=MASTER, baudrate=None):
        if mode != self.MASTER:
            raise NotImplementedError("Only I2C Master supported!")
        _mode = self.MASTER

        #if baudrate != None:
        #    print("I2C frequency is not settable in python, ignoring!")
        
        try:
            self._i2c_bus = smbus.SMBus(bus_num)
        except FileNotFoundError:
            raise RuntimeError("I2C Bus #%d not found, check if enabled in config!" % bus_num)

    def scan(self):
        """Try to read a byte from each address, if you get an OSError it means the device isnt there"""
        found = []
        for addr in range(0,0x80):
            try:
                self._i2c_bus.read_byte(addr)
            except OSError:
                continue
            found.append(addr)
        return found

    def writeto(self, address, buffer, stop=True):
        self._i2c_bus.write_bytes(address, buffer)

    def readfrom_into(self, address, buffer, stop=True):
        readin = self._i2c_bus.read_bytes(address, len(buffer))
        for i in range(len(buffer)):
            buffer[i] = readin[i]
