import gc
from unittest import TestCase
from testing import await_true
gc.collect()


class TestGPSInteractive(TestCase):

    def test_read_value(self):
        import adafruit_blinka
        adafruit_blinka.patch_system() # needed before adafruit_gps imports time

        import microcontroller.pin
        gc.collect()
        import busio
        gc.collect()
        import adafruit_gps
        gc.collect()

        # configure the last available UART (first uart often for REPL)
        uartId, uartTx, uartRx = microcontroller.pin.uartPorts[0]
        uart = busio.UART(uartTx, uartRx, baudrate=9600, timeout=3000)

        gps = adafruit_gps.GPS(uart)

        gps.send_command('PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        gps.send_command('PMTK220,1000')

        def try_fix():
            gps.update()
            return gps.has_fix

        await_true("GPS fix", try_fix)

        self.assertTrue(gps.satellites is not None)
        self.assertTrue(-90 <= gps.latitude < 90)
        self.assertTrue(-180 <= gps.longitude < 180)

