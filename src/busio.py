from adafruit_blinka import Enum, Lockable, agnostic


class SPI(Lockable):
    def __init__(self, clock, MOSI=None, MISO=None):
        from microcontroller import spiPorts
        for spiId, sck, mosi, miso in spiPorts:
            if sck == clock.id and mosi == MOSI.id and miso == MISO.id:
                self._spi = SPI(spiId)
                self._pinIds = (sck, mosi, miso)
                break
        else:
            raise NotImplementedError(
                "No Hardware SPI on (clock, MOSI, MISO)={}\nValid SPI ports:{}".
                format((clock, MOSI, MISO), spiPorts))

    def configure(self, baudrate=100000, polarity=0, phase=0, bits=8):
        if self._locked:
            from machine import Pin
            from microcontroller import spiPorts
            # TODO check if #init ignores MOSI=None rather than unsetting, to save _pinIds attribute
            self._spi.init(
                baudrate=baudrate,
                polarity=polarity,
                phase=phase,
                bits=bits,
                firstbit=SPI.MSB,
                sck=Pin(self._pinIds[0]),
                mosi=Pin(self._pinIds[1]),
                miso=Pin(self._pinIds[2]))
        else:
            raise RuntimeError("First call try_lock()")

    def deinit(self):
        self._spi = None
        self._pinIds = None

    def write(self, buf):
        return self._spi.write(buf)

    def readinto(self, buf):
        return self.readinto(buf)

    def write_readinto(self, buffer_out, buffer_in):
        return self.write_readinto(buffer_out, buffer_in)


class UART(Lockable):
    class Parity(Enum):
        pass

    Parity.ODD = Parity()
    Parity.EVEN = Parity()

    # TODO investigate UART receiver_buffer_size as e.g. read_buf_len in https://github.com/micropython/micropython/blob/3eb0694b97c6a8f0e93b874549aac40d8b78b0e5/ports/stm32/uart.c
    def __init__(self,
                 tx,
                 rx,
                 baudrate=9600,
                 bits=8,
                 parity=None,
                 stop=1,
                 timeout=None,
                 receiver_buffer_size=None,
                 flow=None):
        from microcontroller import uartPorts
        from machine import UART

        self.baudrate = baudrate

        if timeout is not None:  # default 1000
            raise NotImplementedError(
                "Parameter '{}' unsupported on {}".format(
                    "timeout", agnostic.board))
        if receiver_buffer_size is not None:  # default 64
            raise NotImplementedError(
                "Parameter '{}' unsupported on {}".format(
                    "receiver_buffer_size", agnostic.board))
        if flow is not None:  # default 0
            raise NotImplementedError(
                "Parameter '{}' unsupported on {}".format(
                    "flow", agnostic.board))

        # translate parity flag for Micropython
        if parity is UART.Parity.ODD:
            parity = 1
        elif parity is UART.Parity.EVEN:
            parity = 0
        elif parity is None:
            pass
        else:
            raise ValueError("Invalid parity")

        # check tx and rx have hardware support
        for portId, portTx, portRx in uartPorts:  #
            if portTx == tx.id and portRx == rx.id:
                self._uart = UART(
                    portId,
                    baudrate,
                    bits=bits,
                    parity=parity,
                    stop=stop,
                    timeout=timeout)
                break
        else:
            raise NotImplementedError(
                "No Hardware UART on (tx,rx)={}\nValid UART ports".format(
                    (tx, rx), uartPorts))

    def deinit(self):
        self._uart = None

    def read(self, nbytes=None):
        return self._uart.read(nbytes)

    def readinto(self, buf, nbytes=None):
        return self._uart.readinto(buf, nbytes)

    def readline(self):
        return self._uart.readline()

    def write(self, buf):
        return self._uart.write(buf)
