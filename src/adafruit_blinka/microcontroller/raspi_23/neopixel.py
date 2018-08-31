import time
import math
import _rpi_ws281x as ws
import atexit

# LED configuration.
LED_CHANNEL    = 0
LED_FREQ_HZ    = 800000     # Frequency of the LED signal.  We only support 800KHz
LED_DMA_NUM    = 10         # DMA channel to use, can be 0-14.
LED_BRIGHTNESS = 255        # We manage the brightness in the neopixel library
LED_INVERT     = 0          # We don't support inverted logic
LED_STRIP      = ws.WS2811_STRIP_RGB # We manage the color order within the neopixel library

# a 'static' object that we will use to manage our PWM DMA channel
# we only support one LED strip per raspi
_led_strip = None

def neopixel_write(gpio, buf):
    global _led_strip # we'll have one strip we init if its not at first

    if _led_strip is None:
        # Create a ws2811_t structure from the LED configuration.
        # Note that this structure will be created on the heap so you
        # need to be careful that you delete its memory by calling
        # delete_ws2811_t when it's not needed.
        _led_strip = ws.new_ws2811_t()

        # Initialize all channels to off
        for channum in range(2):
            channel = ws.ws2811_channel_get(_led_strip, channum)
            ws.ws2811_channel_t_count_set(channel, 0)
            ws.ws2811_channel_t_gpionum_set(channel, 0)
            ws.ws2811_channel_t_invert_set(channel, 0)
            ws.ws2811_channel_t_brightness_set(channel, 0)

        channel = ws.ws2811_channel_get(_led_strip, LED_CHANNEL)

        # Initialize the channel in use
        ws.ws2811_channel_t_count_set(channel, math.ceil(len(buf)/3)) # we manage 4 vs 3 bytes in the library
        ws.ws2811_channel_t_gpionum_set(channel, gpio._pin.id)
        ws.ws2811_channel_t_invert_set(channel, LED_INVERT)
        ws.ws2811_channel_t_brightness_set(channel, LED_BRIGHTNESS)
        ws.ws2811_channel_t_strip_type_set(channel, LED_STRIP)

        # Initialize the controller
        ws.ws2811_t_freq_set(_led_strip, LED_FREQ_HZ)
        ws.ws2811_t_dmanum_set(_led_strip, LED_DMA_NUM)
    
        resp = ws.ws2811_init(_led_strip)
        if resp != ws.WS2811_SUCCESS:
            message = ws.ws2811_get_return_t_str(resp)
            raise RuntimeError('ws2811_init failed with code {0} ({1})'.format(resp, message))
        if resp == -5:
            print("You'll need to prefix python with 'sudo' to use neopixel_write.")
        atexit.register(neopixel_cleanup)

    channel = ws.ws2811_channel_get(_led_strip, LED_CHANNEL)
    if gpio._pin.id != ws.ws2811_channel_t_gpionum_get(channel):
        raise RuntimeError("Raspberry Pi neopixel support is for one strip only!")

    # assign all colors!
    for i in range(len(buf) // 3):
        r = buf[3*i]
        g = buf[3*i+1]
        b = buf[3*i+2]
        pixel = (r << 16) | (g << 8) | b
        ws.ws2811_led_set(channel, i, pixel)
    
    resp = ws.ws2811_render(_led_strip)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, message))
    if resp == 5:
        print("You'll need to prefix python with 'sudo' to use neopixel_write.")
    time.sleep(0.001 * ((len(buf)//100)+1))  # about 1ms per 100 bytes


def neopixel_cleanup():
    global _led_strip

    if _led_strip is not None:
        # Ensure ws2811_fini is called before the program quits.
        ws.ws2811_fini(_led_strip)
        # Example of calling delete function to clean up structure memory.  Isn't
        # strictly necessary at the end of the program execution here, but is good practice.
        ws.delete_ws2811_t(_led_strip)
        _led_strip = None
