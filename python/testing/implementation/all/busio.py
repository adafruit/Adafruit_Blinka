from unittest import TestCase
from testing import yes_no

class TestMMA8451Interactive(TestCase):

    def test_read_value(self):
        import math
        import board
        gc.collect()
        if not(yes_no("Is MMA8451 wired to SCL {} SDA {} and held still".format(board.SCL, board.SDA))):
            return # test trivially passed
        import busio
        # from https://github.com/adafruit/Adafruit_CircuitPython_MMA8451/blob/29e31a0bb836367bc73763b83513105252b7b264/examples/simpletest.py
        import adafruit_mma8451
        # Initialize I2C bus.
        i2c = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_mma8451.MMA8451(i2c)

        x, y, z = sensor.acceleration
        absolute = math.sqrt(x**2, y**2, z**2)
        self.assertTrue(9 <=absolute <= 11, "Not earth gravity")

        orientation = sensor.orientation
        self.assertTrue(orientation in (
            adafruit_mma8451.PL_PUF,
            adafruit_mma8451.PL_PUB,
            adafruit_mma8451.PL_PDF,
            adafruit_mma8451.PL_PDB,
            adafruit_mma8451.PL_LRF,
            adafruit_mma8451.PL_LRB,
            adafruit_mma8451.PL_LLF,
            adafruit_mma8451.PL_LLB,
        ))

class TestBNO055Interactive(TestCase):

    def test_read_value(self):
        """
        Access all sensor values as per
        https://github.com/adafruit/Adafruit_CircuitPython_BNO055/blob/bdf6ada21e7552c242bc470d4d2619b480b4c574/examples/values.py
        """
        import board
        import busio
        import adafruit_bno055

        i2c = busio.I2C(board.SCL, board.SDA)
        sensor = adafruit_bno055.BNO055(i2c)

        sensor.temperature
        sensor.accelerometer
        sensor.magnetometer
        sensor.gyroscope
        sensor.euler
        sensor.quaternion
        sensor.linear_acceleration
        sensor.gravity


class TestGPSInteractive(TestCase):

    def test_read_value(self):
        import microcontroller
        import busio
        import adafruit_gps

        # configure the last available UART (first uart often for REPL)
        uartId, txId, rxId = microcontroller.uartPorts[-1]
        txPin = microcontroller.Pin(txId)
        rxPin = microcontroller.Pin(rxId)
        uart = busio.UART(txPin, rxPin, baudrate=9600, timeout=3000)

        gps = adafruit_gps.GPS(uart)

        gps.send_command('PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        gps.send_command('PMTK220,1000')
        gps.update()
        self.awaitTrue("GPS fix", lambda: gps.has_fix)
        self.assertTrue(gps.satellites is not None)
        self.assertTrue(-90 <= gps.latitude < 90)
        self.assertTrue(-180 <= gps.longitude < 180)