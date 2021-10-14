"""
Pin definitions for the MacroPad RP2040 with u2if firmware.

Adafruit CircuitPython 6.2.0 on 2021-04-05; Adafruit MacroPad RP2040 with rp2040
>>> import board
>>> board.
KEY1            KEY2            KEY3            KEY4
KEY5            KEY6            KEY7            KEY8
KEY9            KEY10           KEY11           KEY12
LED             SPEAKER_ENABLE  SPEAKER         ENCODER_SWITCH
BUTTON          ENCODER_A       ROTA            ENCODER_B
ROTB            NEOPIXEL        SDA             SCL
OLED_CS         OLED_RESET      OLED_DC         SCLK
SCK             MOSI            MISO            I2C
SPI             UART
"""

from adafruit_blinka.microcontroller.rp2040_u2if import pin

KEY1 = pin.GP1
KEY2 = pin.GP2
KEY3 = pin.GP3
KEY4 = pin.GP4
KEY5 = pin.GP5
KEY6 = pin.GP6
KEY7 = pin.GP7
KEY8 = pin.GP8
KEY9 = pin.GP9
KEY10 = pin.GP10
KEY11 = pin.GP11
KEY12 = pin.GP12

LED = pin.GP13

SPEAKER_ENABLE = pin.GP4
SPEAKER = pin.GP16

ENCODER_SWITCH = BUTTON = pin.GP0

ENCODER_A = ROTA = pin.GP17
ENCODER_B = ROTB = pin.GP18

NEOPIXEL = pin.GP19

SDA = pin.GP20
SCL = pin.GP21

OLED_CS = pin.GP22
OLED_RESET = pin.GP23
OLED_DC = pin.GP24

SCLK = SCK = pin.GP26
MOSI = pin.GP27
MISO = pin.GP28

# access u2if via pin instance to open for specifc VID/PID
# pylint:disable = protected-access
pin.GP0._u2if_open_hid(0x239A, 0x0107)
