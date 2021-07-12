"""Pin definitions for the Raspberry Pi Pico running u2if firmware"""
from adafruit_blinka.microcontroller.rp2040_u2if import pin

GP0 = pin.GP0
GP1 = pin.GP1
GP2 = pin.GP2
GP3 = pin.GP3
GP4 = pin.GP4
GP5 = pin.GP5
GP6 = pin.GP6
GP7 = pin.GP7
GP8 = pin.GP8
GP9 = pin.GP9
GP10 = pin.GP10
GP11 = pin.GP11
GP12 = pin.GP12
GP13 = pin.GP13
GP14 = pin.GP14
GP15 = pin.GP15
GP16 = pin.GP16
GP17 = pin.GP17
GP18 = pin.GP18
GP19 = pin.GP19
GP20 = pin.GP20
GP21 = pin.GP21
GP22 = pin.GP22
GP26 = pin.GP26
GP27 = pin.GP27
GP28 = pin.GP28

ADC0 = GP26
ADC1 = GP27

SCL = SCL0 = GP5
SDA = SDA0 = GP4

SCL1 = GP15
SDA1 = GP14

SCLK = SCK = SCLK0 = SCK0 = GP18
MOSI = MOSI0 = GP19
MISO = MISO0 = GP12

SCLK1 = SCK1 = GP10
MOSI1 = GP11
MISO1 = GP12

# access u2if via pin instance to open for specifc VID/PID
# pylint:disable = protected-access
pin.GP0._u2if_open_hid(0xCAFE, 0x4005)
