# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""SPI Class for Binho Nova"""
from adafruit_blinka.microcontroller.nova import Connection


class SPI:
    """Custom SPI Class for Binho Nova"""

    MSB = 0
    BUFFER_PAYLOAD_MAX_LENGTH = 64
    WHR_PAYLOAD_MAX_LENGTH = 1024

    def __init__(self, clock):
        self._nova = Connection.getInstance()
        self._nova.setNumericalBase(10)
        self._nova.setOperationMode(0, "SPI")
        self._nova.setClockSPI(0, clock)
        self._nova.setModeSPI(0, 0)
        self._nova.setIOpinMode(0, "DOUT")
        self._nova.setIOpinMode(1, "DOUT")
        self._nova.beginSPI(0)
        self._novaCMDVer = "0"
        if hasattr(self._nova, "getCommandVer"):
            response = self._nova.getCommandVer().split(" ")
            if response[0] != "-NG":
                self._novaCMDVer = response[1]

        # Cpol and Cpha set by mode
        # Mode  Cpol Cpha
        #  0     0    0
        #  1     0    1
        #  2     1    0
        #  3     1    1

    def __del__(self):
        """Close Nova on delete"""
        self._nova.close()

    # pylint: disable=too-many-arguments,unused-argument
    def init(
        self,
        baudrate=1000000,
        polarity=0,
        phase=0,
        bits=8,
        firstbit=MSB,
        sck=None,
        mosi=None,
        miso=None,
    ):
        """Initialize the Port"""
        self._nova.setClockSPI(0, baudrate)
        self._nova.setModeSPI(0, (polarity << 1) | (phase))

    # pylint: enable=too-many-arguments,unused-argument

    @staticmethod
    def get_received_data(lineOutput):
        """Return any received data"""
        return lineOutput.split("RXD ")[1]

    @property
    def frequency(self):
        """Return the current frequency"""
        return self._nova.getClockSPI(0).split("CLK ")[1]

    def write(self, buf, start=0, end=None):
        """Write data from the buffer to SPI"""
        end = end if end else len(buf)
        payloadMaxLength = self.BUFFER_PAYLOAD_MAX_LENGTH
        if int(self._novaCMDVer) >= 1:
            payloadMaxLength = self.WHR_PAYLOAD_MAX_LENGTH
        chunks, rest = divmod(end - start, payloadMaxLength)

        for i in range(chunks):
            chunk_start = start + i * payloadMaxLength
            chunk_end = chunk_start + payloadMaxLength
            if int(self._novaCMDVer) >= 1:
                self._nova.writeToReadFromSPI(
                    0, True, False, chunk_end - chunk_start, buf[chunk_start:chunk_end]
                )
            else:
                self._nova.clearBuffer(0)
                self._nova.writeToBuffer(0, 0, buf[chunk_start:chunk_end])
                self._nova.transferBufferSPI(0, chunk_end - chunk_start + 1)
        if rest:
            if int(self._novaCMDVer) >= 1:
                self._nova.writeToReadFromSPI(0, True, False, rest, buf[-1 * rest :])
            else:
                self._nova.clearBuffer(0)
                self._nova.writeToBuffer(0, 0, buf[-1 * rest :])
                self._nova.transferBufferSPI(0, rest)

    def readinto(self, buf, start=0, end=None, write_value=0):
        """Read data from SPI and into the buffer"""
        end = end if end else len(buf)
        if int(self._novaCMDVer) >= 1:
            chunks, rest = divmod(end - start, self.WHR_PAYLOAD_MAX_LENGTH)
            i = 0
            for i in range(chunks):
                chunk_start = start + i * self.WHR_PAYLOAD_MAX_LENGTH
                chunk_end = chunk_start + self.WHR_PAYLOAD_MAX_LENGTH
                result = self._nova.writeToReadFromSPI(
                    0, False, True, chunk_end - chunk_start, write_value
                )
                if result != "-NG":
                    resp = result.split(" ")
                    resp = resp[2]
                    # loop over half of resp len as we're reading 2 chars at a time to form a byte
                    loops = int(len(resp) / 2)
                    for j in range(loops):
                        buf[(i * self.WHR_PAYLOAD_MAX_LENGTH) + start + j] = int(
                            resp[j * 2] + resp[j * 2 + 1], 16
                        )
                else:
                    raise RuntimeError(
                        "Received error response from Binho Nova, result = " + result
                    )
            if rest:
                result = self._nova.writeToReadFromSPI(
                    0, False, True, rest, write_value
                )
                if result != "-NG":
                    resp = result.split(" ")
                    resp = resp[2]

                    # loop over half of resp len as we're reading 2 chars at a time to form a byte
                    loops = int(len(resp) / 2)
                    for j in range(loops):
                        buf[(i * self.WHR_PAYLOAD_MAX_LENGTH) + start + j] = int(
                            resp[j * 2] + resp[j * 2 + 1], 16
                        )
                else:
                    raise RuntimeError(
                        "Received error response from Binho Nova, result = " + result
                    )
        else:
            for i in range(start, end):
                buf[start + i] = int(
                    self.get_received_data(self._nova.transferSPI(0, write_value))
                )

    # pylint: disable=too-many-arguments,too-many-locals,too-many-branches
    def write_readinto(
        self, buffer_out, buffer_in, out_start=0, out_end=None, in_start=0, in_end=None
    ):
        """Perform a half-duplex write from buffer_out and then
        read data into buffer_in
        """
        out_end = out_end if out_end else len(buffer_out)
        in_end = in_end if in_end else len(buffer_in)
        readlen = in_end - in_start
        writelen = out_end - out_start
        if readlen > writelen:
            # resize out and pad with 0's
            tmp = bytearray(buffer_out)
            tmp.extend([0] * (readlen - len(buffer_out)))
            buffer_out = tmp

        if int(self._novaCMDVer) >= 1:
            chunks, rest = divmod(len(buffer_out), self.WHR_PAYLOAD_MAX_LENGTH)
            i = 0
            for i in range(chunks):
                chunk_start = out_start + i * self.WHR_PAYLOAD_MAX_LENGTH
                chunk_end = chunk_start + self.WHR_PAYLOAD_MAX_LENGTH
                result = self._nova.writeToReadFromSPI(
                    0,
                    True,
                    True,
                    chunk_end - chunk_start,
                    buffer_out[chunk_start:chunk_end],
                )

                if result != "-NG":
                    resp = result.split(" ")
                    resp = resp[2]

                    # loop over half of resp len as we're reading 2 chars at a time to form a byte
                    loops = int(len(resp) / 2)
                    for j in range(loops):
                        buffer_in[
                            (i * self.WHR_PAYLOAD_MAX_LENGTH) + in_start + j
                        ] = int(resp[j * 2] + resp[j * 2 + 1], 16)
                else:
                    raise RuntimeError(
                        "Received error response from Binho Nova, result = " + result
                    )
            if rest:
                result = self._nova.writeToReadFromSPI(
                    0, True, True, rest, buffer_out[-1 * rest :]
                )
                if result != "-NG":
                    resp = result.split(" ")
                    resp = resp[2]

                    # loop over half of resp len as we're reading 2 chars at a time to form a byte
                    loops = int(len(resp) / 2)
                    for j in range(loops):
                        buffer_in[
                            (i * self.WHR_PAYLOAD_MAX_LENGTH) + in_start + j
                        ] = int(resp[j * 2] + resp[j * 2 + 1], 16)
                else:
                    raise RuntimeError(
                        "Received error response from Binho Nova, result = " + result
                    )
            print(buffer_in)
        else:
            for data_out in buffer_out:
                data_in = int(
                    self.get_received_data(self._nova.transferSPI(0, data_out))
                )
                if i < readlen:
                    buffer_in[in_start + i] = data_in
                i += 1

    # pylint: enable=too-many-arguments,too-many-locals,too-many-branches
