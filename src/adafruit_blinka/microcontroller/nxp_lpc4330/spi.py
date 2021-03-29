"""SPI Class for NXP LPC4330"""
from greatfet import GreatFET


class SPI:
    """Custom I2C Class for NXP LPC4330"""

    MSB = 0

    def __init__(self):
        self._gf = GreatFET()
        self._frequency = None
        self.buffer_size = 255
        self._mode = 0
        self._spi = None
        self._presets = {
            204000: (100, 9),
            408000: (100, 4),
            680000: (100, 2),
            1020000: (100, 1),
            2040000: (50, 1),
            4250000: (24, 1),
            8500000: (12, 1),
            12750000: (8, 1),
            17000000: (6, 1),
            20400000: (2, 4),
            25500000: (4, 1),
            34000000: (2, 2),
            51000000: (2, 1),
            102000000: (2, 0),
        }

    # pylint: disable=too-many-arguments,unused-argument
    def init(
        self,
        baudrate=100000,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=MSB,
        sck=None,
        mosi=None,
        miso=None,
    ):
        """Initialize the Port"""
        # Figure out the mode based on phase and polarity
        polarity = int(polarity)
        phase = int(phase)
        self._mode = (polarity << 1) | phase

        # Using API due to possible interface change
        self._spi = self._gf.apis.spi
        # Check baudrate against presets and adjust to the closest one
        if self._frequency is None:
            preset = self._find_closest_preset(baudrate)
        else:
            preset = self._presets[self._frequency]
        clock_prescale_rate, serial_clock_rate = preset
        self._spi.init(serial_clock_rate, clock_prescale_rate)

        # Set the polarity and phase (the "SPI mode").
        self._spi.set_clock_polarity_and_phase(self._mode)

    # pylint: enable=too-many-arguments

    def _find_closest_preset(self, target_frequency):
        """Loop through self._frequencies and find the closest
        setting. Return the preset values and set the frequency
        to the found value
        """
        closest_preset = None
        for frequency in self._presets:
            preset = self._presets[frequency]
            if self._frequency is None or abs(frequency - target_frequency) < abs(
                self._frequency - target_frequency
            ):
                self._frequency = frequency
                closest_preset = preset

        return closest_preset

    @property
    def frequency(self):
        """Return the current frequency"""
        return self._frequency

    def write(self, buf, start=0, end=None):
        """Write data from the buffer to SPI"""
        end = end if end else len(buf)
        self._transmit(buf[start:end])

    # pylint: disable=unused-argument
    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read data from SPI and into the buffer"""
        end = end if end else len(buf)
        result = self._transmit([write_value] * (end - start), end - start)
        for i, b in enumerate(result):
            buf[start + i] = b

    # pylint: enable=unused-argument

    # pylint: disable=too-many-arguments
    def write_readinto(
        self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None
    ):
        """Perform a half-duplex write from buffer_out and then
        read data into buffer_in
        """
        out_end = out_end if out_end else len(buffer_out)
        in_end = in_end if in_end else len(buffer_in)

        result = self._transmit(buffer_out[out_start:out_end], in_end - in_start)
        for i, b in enumerate(result):
            buffer_in[in_start + i] = b

    # pylint: enable=too-many-arguments

    def _transmit(self, data, receive_length=None):
        data_to_transmit = bytearray(data)
        data_received = bytearray()

        if receive_length is None:
            receive_length = len(data)

        # If we need to receive more than we've transmitted, extend the data out.
        if receive_length > len(data):
            padding = receive_length - len(data)
            data_to_transmit.extend([0] * padding)

        # Transmit our data in chunks of the buffer size.
        while data_to_transmit:
            # Extract a single data chunk from the transmit buffer.
            chunk = data_to_transmit[0 : self.buffer_size]
            del data_to_transmit[0 : self.buffer_size]

            # Finally, exchange the data.
            response = self._spi.clock_data(len(chunk), bytes(chunk))
            data_received.extend(response)

        # Once we're done, return the data received.
        return bytes(data_received)
