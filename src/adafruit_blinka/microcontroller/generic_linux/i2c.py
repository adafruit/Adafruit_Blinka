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

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        if end is None:
            end = len(buffer)
        self._i2c_bus.write_bytes(address, buffer[start:end])

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
        if end is None:
            end = len(buffer)
        
        readin = self._i2c_bus.read_bytes(address, end-start)
        for i in range(end-start):
            buffer[i+start] = readin[i]

    def writeto_then_readfrom(self, address, buffer_out, buffer_in, *,
                       out_start=0, out_end=None,
                       in_start=0, in_end=None, stop=False):
        if out_end is None:
            out_end = len(buffer_out)        
        if in_end is None:
            in_end = len(buffer_in)
        if stop:
            # To generate a stop in linux, do in two transactions
            self.writeto(address, buffer_out, start=out_start, end=out_end, stop=True)
            self.readfrom_into(address, buffer_in, start=in_start, end=in_end)
        else:
            # To generate without a stop, do in one block transaction
            if out_end-out_start != 1:
                raise NotImplementedError("Currently can only write a single byte in writeto_then_readfrom")
            readin = self._i2c_bus.read_i2c_block_data(address, buffer_out[out_start:out_end][0], in_end-in_start)
            for i in range(in_end-in_start):
                buffer_in[i+in_start] = readin[i]

