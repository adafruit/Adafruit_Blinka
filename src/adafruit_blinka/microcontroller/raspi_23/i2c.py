import smbus
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

        if baudrate != None:
            print("I2C frequency is not settable in python, ignoring!")
        
        try:
            self._i2c_bus = smbus.SMBus(bus_num)
        except FileNotFoundError:
            raise RuntimeError("I2C Bus #%d not found, check if enabled in config!" % bus_num)

    def scan(self):
        found = []
        for addr in range(0,0x7F):
            try:
                self._i2c_bus.read_byte(addr)
            except OSError:
                continue
            found.append(addr)
        return found
