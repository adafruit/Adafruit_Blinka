"""I2C Class for Binho Nova"""

from adafruit_blinka.microcontroller.nova import Connection


class I2C:
    """Custom I2C Class for Binho Nova"""

    WHR_PAYLOAD_MAX_LENGTH = 1024

    def __init__(self, *, frequency=400000):
        self._nova = Connection.getInstance()
        self._nova.setNumericalBase(10)
        self._nova.setOperationMode(0, "I2C")
        self._nova.setPullUpStateI2C(0, "EN")
        self._nova.setClockI2C(0, frequency)

        self._novaCMDVer = "0"
        if hasattr(self._nova, "getCommandVer"):
            response = self._nova.getCommandVer().split(" ")
            if response[0] != "-NG":
                self._novaCMDVer = response[1]

    def __del__(self):
        """Close Nova on delete"""
        self._nova.close()

    def scan(self):
        """Perform an I2C Device Scan"""
        scanResults = []

        for i in range(8, 121):
            result = self._nova.scanAddrI2C(0, i << 1)

            resp = result.split(" ")

            if resp[3] == "OK":
                scanResults.append(i)

        return scanResults

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        """Write data from the buffer to an address"""
        end = end if end else len(buffer)
        readBytes = 0
        if int(self._novaCMDVer) >= 1:
            chunks, rest = divmod(end - start, self.WHR_PAYLOAD_MAX_LENGTH)
            for i in range(chunks):
                chunk_start = start + i * self.WHR_PAYLOAD_MAX_LENGTH
                chunk_end = chunk_start + self.WHR_PAYLOAD_MAX_LENGTH
                self._nova.writeToReadFromI2C(
                    0,
                    address << 1,
                    stop,
                    readBytes,
                    chunk_end - chunk_start,
                    buffer[chunk_start:chunk_end],
                )
            if rest:
                self._nova.writeToReadFromI2C(
                    0, address << 1, stop, readBytes, rest, buffer[-1 * rest :]
                )
        else:
            self._nova.startI2C(0, address << 1)

            for i in range(start, end):
                self._nova.writeByteI2C(0, buffer[i])

            if stop:
                self._nova.endI2C(0)
            else:
                self._nova.endI2C(0, True)

    # pylint: disable=unused-argument
    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):
        """Read data from an address and into the buffer"""
        end = end if end else len(buffer)
        result = self._nova.readBytesI2C(0, address << 1, len(buffer[start:end]))

        if result != "-NG":
            resp = result.split(" ")

            for i in range(len(buffer[start:end])):
                buffer[start + i] = int(resp[2 + i])
        else:
            raise RuntimeError(
                "Received error response from Binho Nova, result = " + result
            )

    # pylint: disable=too-many-locals,too-many-branches
    def writeto_then_readfrom(
        self,
        address,
        buffer_out,
        buffer_in,
        *,
        out_start=0,
        out_end=None,
        in_start=0,
        in_end=None,
        stop=False
    ):
        """Write data from buffer_out to an address and then
        read data from an address and into buffer_in
        """
        out_end = out_end if out_end else len(buffer_out)
        in_end = in_end if in_end else len(buffer_in)
        if int(self._novaCMDVer) >= 1:
            totalIn = in_end - in_start
            totalOut = out_end - out_start
            totalBytes = totalIn
            if totalOut > totalIn:
                totalBytes = totalOut
            chunks, rest = divmod(totalBytes, self.WHR_PAYLOAD_MAX_LENGTH)
            if rest > 0:
                chunks += 1

            for i in range(chunks):
                # calculate the number of bytes to be written and read
                numInBytes = self.WHR_PAYLOAD_MAX_LENGTH
                if totalIn < self.WHR_PAYLOAD_MAX_LENGTH:
                    numInBytes = totalIn
                numOutBytes = self.WHR_PAYLOAD_MAX_LENGTH
                if totalOut < self.WHR_PAYLOAD_MAX_LENGTH:
                    numOutBytes = totalOut

                # setup the buffer out chunk offset
                buffer = "0"
                if numOutBytes > 0:
                    chunk_start = out_start + i * self.WHR_PAYLOAD_MAX_LENGTH
                    chunk_end = chunk_start + numOutBytes
                    buffer = buffer_out[chunk_start:chunk_end]

                result = self._nova.writeToReadFromI2C(
                    0, address << 1, stop, numInBytes, numOutBytes, buffer
                )
                totalIn -= numInBytes
                totalOut -= numOutBytes

                if result != "-NG":
                    if numInBytes:
                        resp = result.split(" ")
                        resp = resp[2]

                        for j in range(numInBytes):
                            buffer_in[
                                in_start + i * self.WHR_PAYLOAD_MAX_LENGTH + j
                            ] = int(resp[j * 2] + resp[j * 2 + 1], 16)
                else:
                    raise RuntimeError(
                        "Received error response from Binho Nova, result = " + result
                    )
        else:
            self._nova.startI2C(0, address << 1)

            for i in range(out_start, out_end):
                self._nova.writeByteI2C(0, buffer_out[i])

            if stop:
                self._nova.endI2C(0)
            else:
                self._nova.endI2C(0, True)

            result = self._nova.readBytesI2C(
                0, address << 1, len(buffer_in[in_start:in_end])
            )

            if result != "-NG":
                resp = result.split(" ")

                for i in range(len(buffer_in[in_start:in_end])):
                    buffer_in[in_start + i] = int(resp[2 + i])
            else:
                raise RuntimeError(
                    "Received error response from Binho Nova, result = " + result
                )


# pylint: enable=unused-argument,too-many-locals,too-many-branches
