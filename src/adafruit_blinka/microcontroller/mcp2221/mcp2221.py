import time
import hid

class MCP2221:

    VID = 0x04D8
    PID = 0x00DD

    GP_GPIO = 0b000
    GP_DEDICATED = 0b001
    GP_ALT0 = 0b010
    GP_ALT1 = 0b011
    GP_ALT2 = 0b100

    def __init__(self):
        self._hid = hid.device()
        self._hid.open(MCP2221.VID, MCP2221.PID)

    def _hid_xfer(self, report, response=True):
        # first byte is report ID, which =0 for MCP2221
        # remaing bytes = 64 byte report data
        # https://github.com/libusb/hidapi/blob/083223e77952e1ef57e6b77796536a3359c1b2a3/hidapi/hidapi.h#L185
        self._hid.write(b'\0' + report + b'\0'*(64-len(report)))
        if response:
            # return is 64 byte response report
            return self._hid.read(64)

    #----------------------------------------------------------------
    # MISC
    #----------------------------------------------------------------
    def gp_get_mode(self, pin):
        return self._hid_xfer(bytes([0x61]))[22+pin] & 0x07

    def gp_set_mode(self, pin, mode):
        # get current settings
        current = self._hid_xfer(bytes([0x61]))
        # empty report, this is safe since 0's = no change
        report = bytearray([0x60]+[0]*63)
        # set the alter GP flag byte
        report[7] = 0xFF
        # each pin can be set individually
        # but all 4 get set at once, so we need to
        # transpose current settings
        report[8]  = current[22]  # GP0
        report[9]  = current[23]  # GP1
        report[10] = current[24]  # GP2
        report[11] = current[25]  # GP3
        # then change only the one
        report[8+pin] = mode & 0x07
        # and make it so
        self._hid_xfer(report)

    def _pretty_report(self, report):
        print("     0  1  2  3  4  5  6  7  8  9")
        index = 0
        for row in range(7):
            print("{} : ".format(row), end='')
            for _ in range(10):
                print("{:02x} ".format(report[index]), end='')
                index += 1
                if index > 63:
                    break
            print()

    def _status_dump(self):
        self._pretty_report(self._hid_xfer(bytes([0x10])))

    def _sram_dump(self):
        self._pretty_report(self._hid_xfer(bytes([0x61])))

    def _reset(self):
        self._hid_xfer(b'\x70\xAB\xCD\xEF', response=False)
        time.sleep(1)
        self._hid.open(MCP2221.VID, MCP2221.PID)

    #----------------------------------------------------------------
    # GPIO
    #----------------------------------------------------------------
    def gpio_set_direction(self, pin, mode):
        report = bytearray([0x50]+[0]*63)  # empty set GPIO report
        offset = 4 * (pin + 1)
        report[offset] = 0x01              # set pin direction
        report[offset+1] = mode            # to this
        self._hid_xfer(report)

    def gpio_set_pin(self, pin, value):
        report = bytearray([0x50]+[0]*63)  # empty set GPIO report
        offset = 2 + 4 * pin
        report[offset] = 0x01              # set pin value
        report[offset+1] = value           # to this
        self._hid_xfer(report)

    def gpio_get_pin(self, pin):
        resp = self._hid_xfer(bytes([0x51]))
        offset = 2 + 2 * pin
        if resp[offset] == 0xEE:
            raise RuntimeError("Pin is not set for GPIO operation.")
        else:
            return resp[offset]

    #----------------------------------------------------------------
    # I2C
    #
    # cribbed from the C driver:
    #   define RESP_ERR_NOERR          0x00
    #   define RESP_ADDR_NACK          0x25
    #   define RESP_READ_ERR           0x7F
    #   define RESP_READ_COMPL         0x55
    #   define RESP_I2C_IDLE           0x00
    #   define RESP_I2C_START_TOUT     0x12
    #   define RESP_I2C_RSTART_TOUT    0x17
    #   define RESP_I2C_WRADDRL_TOUT   0x23
    #   define RESP_I2C_WRADDRL_WSEND  0x21
    #   define RESP_I2C_WRADDRL_NACK   0x25
    #   define RESP_I2C_WRDATA_TOUT    0x44
    #   define RESP_I2C_RDDATA_TOUT    0x52
    #   define RESP_I2C_STOP_TOUT      0x62
    #----------------------------------------------------------------
    def i2c_configure(self, baudrate=100000):
        self._hid_xfer(bytes([0x10,  # set parameters
                              0x00,  # don't care
                              0x00,  # no effect
                              0x20,  # next byte is clock divider
                              12000000 // baudrate - 3]))

    def i2c_writeto(self, address, buffer, *, start=0, end=None):
        end = end if end else len(buffer)
        self._hid_xfer(bytes([0x90,                    # i2c write data
                              end - start & 0xFF,      # xfer length lo byte
                              end - start >> 8 & 0xFF, # xfer length hi byte
                              address << 1]) +         # i2c slave address
                              buffer[start:end])       # user data to be sent

    def i2c_readfrom_into(self, address, buffer, *, start=0, end=None):
        end = end if end else len(buffer)
        retries = 0
        while retries < 5:
            #
            # why does this require two xfers?
            #
            # 1. tell it we want to read
            self._hid_xfer(bytes([0x91,                     # i2c read data
                                  end - start & 0xFF,       # xfer length lo byte
                                  end - start >> 8 & 0xFF,  # xfer length hi byte
                                  address << 1 | 0x01]))    # i2c slave address
            # 2. and then actually read
            response = self._hid_xfer(bytes([0x40]))
            # check for success
            if response[1] == 0x00:
                break
            retries += 1
        if retries >= 5:
            raise RuntimeError("I2C read error, max retries reached.")
        # move data into buffer
        for i in range(end - start):
            buffer[start + i] = response[4 + i]

    def i2c_writeto_then_readfrom(self, address, out_buffer, in_buffer, *,
                                  out_start=0, out_end=None,
                                  in_start=0, in_end=None):
        out_end = out_end if out_end else len(buffer_out)
        in_end = in_end if in_end else len(buffer_in)
        self._hid_xfer(bytes([0x94,                            # i2c write data no stop
                              out_end - out_start & 0xFF,      # xfer length lo byte
                              out_end - out_start >> 8 & 0xFF, # xfer length hi byte
                              address << 1]) +                 # i2c slave address
                              out_buffer[out_start:out_end])   # user data to be sent
        retries = 5
        while retries < 5:
            #
            # why does this require two xfers?
            #
            # 1. tell it we want to read
            self._hid_xfer(bytes([0x93,                           # i2c read data repeated start
                                  in_end - in_start & 0xFF,       # xfer length lo byte
                                  in_end - in_start >> 8 & 0xFF,  # xfer length hi byte
                                  address << 1 | 0x01]))          # i2c slave address
            # 2. and then actually read
            response = self._hid_xfer(bytes([0x40]))
            # check for success
            if response[1] == 0x00:
                break
            retries += 1
        if retries >= 5:
            raise RuntimeError("I2C read error, max retries reached.")
        # move data into buffer
        for i in range(in_end - in_start):
            in_buffer[in_start + i] = response[4 + i]

    def i2c_scan(self, *, start=0, end=0x79):
        found = []
        for addr in range(start, end+1):
            # try a write
            self.i2c_writeto(addr, b'\x00')
            # store if success
            if self._hid_xfer(b'\x10')[8] == 0x00:
                found.append(addr)
            # cancel and continue
            self._hid_xfer(b'\x10\x00\x10')
        return found

    #----------------------------------------------------------------
    # ADC
    #----------------------------------------------------------------
    def adc_configure(self, vref=0):
        report = bytearray([0x60]+[0]*63)
        report[5] = 1 << 7 | (vref & 0b111)
        self._hid_xfer(report)

    def adc_read(self, pin):
        resp = self._hid_xfer(bytes([0x10]))
        return resp[49 + 2 * pin] << 8 | resp[48 + 2 * pin]

    #----------------------------------------------------------------
    # DAC
    #----------------------------------------------------------------
    def dac_configure(self, vref=0):
        report = bytearray([0x60]+[0]*63)
        report[3] = 1 << 7 | (vref & 0b111)
        self._hid_xfer(report)

    def dac_write(self, pin, value):
        report = bytearray([0x60]+[0]*63)
        report[4] = 1 << 7 | (value & 0b11111)
        self._hid_xfer(report)

mcp2221 = MCP2221()
