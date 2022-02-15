import gc
from testing import yes_no

gc.collect()
from unittest import TestCase

gc.collect()
from testing.board.i2c import I2C

gc.collect()


class TestBME280Interactive(TestCase):
    def test_read_value(self):

        import board

        gc.collect()
        import adafruit_bme280

        gc.collect()

        if not (
            yes_no("Is BME280 wired to SCL {} SDA {}".format(board.SCL, board.SDA))
        ):
            return  # test trivially passed

        i2c = I2C(board.SCL, board.SDA)
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        temperature = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure
        altitude = bme280.altitude
        self.assertTrue(type(temperature) is float)
        self.assertTrue(type(humidity) is float)
        self.assertTrue(type(pressure) is float)
        self.assertTrue(type(altitude) is float)

        self.assertTrue(-50 <= temperature <= 50)
        self.assertTrue(0 <= humidity <= 100)
        self.assertTrue(900 <= pressure <= 1100)
        self.assertTrue(-1000 <= altitude <= 9, 848)


class TestMMA8451Interactive(TestCase):
    def test_read_value(self):
        import math

        gc.collect()
        import board

        gc.collect()

        if not (
            yes_no(
                "Is MMA8451 wired to SCL {} SDA {} and held still".format(
                    board.SCL, board.SDA
                )
            )
        ):
            return  # test trivially passed
        # from https://github.com/adafruit/Adafruit_CircuitPython_MMA8451/blob/29e31a0bb836367bc73763b83513105252b7b264/examples/simpletest.py
        import adafruit_mma8451

        i2c = I2C(board.SCL, board.SDA)
        sensor = adafruit_mma8451.MMA8451(i2c)

        x, y, z = sensor.acceleration
        absolute = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        self.assertTrue(9 <= absolute <= 11, "Not earth gravity")

        orientation = sensor.orientation
        self.assertTrue(
            orientation
            in (
                adafruit_mma8451.PL_PUF,
                adafruit_mma8451.PL_PUB,
                adafruit_mma8451.PL_PDF,
                adafruit_mma8451.PL_PDB,
                adafruit_mma8451.PL_LRF,
                adafruit_mma8451.PL_LRB,
                adafruit_mma8451.PL_LLF,
                adafruit_mma8451.PL_LLB,
            )
        )


class TestBNO055Interactive(TestCase):
    def test_read_value(self):
        """
        Access all sensor values as per
        https://github.com/adafruit/Adafruit_CircuitPython_BNO055/blob/bdf6ada21e7552c242bc470d4d2619b480b4c574/examples/values.py
        Note I have not successfully run this test. Possibly a hardware issue with module I have.
        See https://forums.adafruit.com/viewtopic.php?f=60&t=131665
        """
        import board

        gc.collect()
        import adafruit_bno055

        gc.collect()
        i2c = I2C(board.SCL, board.SDA)
        sensor = adafruit_bno055.BNO055(i2c)

        self.assertTrue(9 <= sensor.gravity <= 11)
        self.assertTrue(sensor.temperature != 0)
        self.assertTrue(sensor.acceleration != (0, 0, 0))
        self.assertTrue(sensor.magnetometer != (0, 0, 0))
        self.assertTrue(sensor.gyroscope != (0, 0, 0))
        self.assertTrue(sensor.quaternion != (0, 0, 0, 0))
        sensor.euler
        sensor.linear_acceleration
