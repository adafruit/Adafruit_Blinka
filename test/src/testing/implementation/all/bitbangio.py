import gc
from testing import yes_no
gc.collect()
from unittest import TestCase
gc.collect()

class TestBME280Interactive(TestCase):

    def test_read_value(self):
        import board
        gc.collect()
        if not(yes_no("Is BME280 wired to SCL {} SDA {}".format(board.SCL, board.SDA))):
            return # test trivially passed

        import board
        gc.collect()
        import bitbangio
        gc.collect()
        import adafruit_bme280
        gc.collect()
        i2c = bitbangio.I2C(board.SCL, board.SDA)
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        temperature = bme280.temperature
        humidity = bme280.humidity
        pressure = bme280.pressure
        altitude = bme280.altitude
        self.assertTrue(type(temperature) is float )
        self.assertTrue(type(humidity) is float )
        self.assertTrue(type(pressure) is float )
        self.assertTrue(type(altitude) is float )

        self.assertTrue( -50 <= temperature <= 50)
        self.assertTrue( 0 <= humidity <= 100)
        self.assertTrue( 900 <= pressure <= 1100)
        self.assertTrue( -1000 <= altitude <= 9,848)
