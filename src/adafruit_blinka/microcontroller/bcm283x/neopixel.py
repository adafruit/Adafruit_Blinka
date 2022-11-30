# SPDX-FileCopyrightText: 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""BCM283x NeoPixel Driver Class"""
import time
import atexit
import _rpi_ws281x as ws

# LED configuration.
# pylint: disable=redefined-outer-name,too-many-branches,too-many-statements
# pylint: disable=global-statement,protected-access
LED_CHANNEL = 0
LED_FREQ_HZ = 800000  # Frequency of the LED signal.  We only support 800KHz
LED_DMA_NUM = 10  # DMA channel to use, can be 0-14.
LED_BRIGHTNESS = 255  # We manage the brightness in the neopixel library
LED_INVERT = 0  # We don't support inverted logic
LED_STRIP = None  # We manage the color order within the neopixel library

# a 'static' object that we will use to manage our PWM DMA channel
# we only support one LED strip per raspi
_led_strip = None
_buf = None


def neopixel_write(gpio, buf):
    """NeoPixel Writing Function"""
    global _led_strip  # we'll have one strip we init if its not at first
    global _buf  # we save a reference to the buf, and if it changes we will cleanup and re-init.

    if _led_strip is None or buf is not _buf:
        # This is safe to call since it doesn't do anything if _led_strip is None
        neopixel_cleanup()

        # Create a ws2811_t structure from the LED configuration.
        # Note that this structure will be created on the heap so you
        # need to be careful that you delete its memory by calling
        # delete_ws2811_t when it's not needed.
        _led_strip = ws.new_ws2811_t()
        _buf = buf

        # Initialize all channels to off
        for channum in range(2):
            channel = ws.ws2811_channel_get(_led_strip, channum)
            ws.ws2811_channel_t_count_set(channel, 0)
            ws.ws2811_channel_t_gpionum_set(channel, 0)
            ws.ws2811_channel_t_invert_set(channel, 0)
            ws.ws2811_channel_t_brightness_set(channel, 0)

        channel = ws.ws2811_channel_get(_led_strip, LED_CHANNEL)

        # Initialize the channel in use
        count = 0
        if len(buf) % 3 == 0:
            # most common, divisible by 3 is likely RGB
            LED_STRIP = ws.WS2811_STRIP_RGB
            count = len(buf) // 3
        elif len(buf) % 4 == 0:
            LED_STRIP = ws.SK6812_STRIP_RGBW
            count = len(buf) // 4
        else:
            raise RuntimeError("We only support 3 or 4 bytes-per-pixel")

        ws.ws2811_channel_t_count_set(
            channel, count
        )  # we manage 4 vs 3 bytes in the library
        ws.ws2811_channel_t_gpionum_set(channel, gpio._pin.id)
        ws.ws2811_channel_t_invert_set(channel, LED_INVERT)
        ws.ws2811_channel_t_brightness_set(channel, LED_BRIGHTNESS)
        ws.ws2811_channel_t_strip_type_set(channel, LED_STRIP)

        # Initialize the controller
        ws.ws2811_t_freq_set(_led_strip, LED_FREQ_HZ)
        ws.ws2811_t_dmanum_set(_led_strip, LED_DMA_NUM)

        resp = ws.ws2811_init(_led_strip)
        if resp != ws.WS2811_SUCCESS:
            if resp == -5:
                raise RuntimeError(
                    "NeoPixel support requires running with sudo, please try again!"
                )
            message = ws.ws2811_get_return_t_str(resp)
            raise RuntimeError(
                "ws2811_init failed with code {0} ({1})".format(resp, message)
            )
        atexit.register(neopixel_cleanup)

    channel = ws.ws2811_channel_get(_led_strip, LED_CHANNEL)
    if gpio._pin.id != ws.ws2811_channel_t_gpionum_get(channel):
        raise RuntimeError("Raspberry Pi neopixel support is for one strip only!")

    if ws.ws2811_channel_t_strip_type_get(channel) == ws.WS2811_STRIP_RGB:
        bpp = 3
    else:
        bpp = 4
    # assign all colors!
    for i in range(len(buf) // bpp):
        r = buf[bpp * i]
        g = buf[bpp * i + 1]
        b = buf[bpp * i + 2]
        if bpp == 3:
            pixel = (r << 16) | (g << 8) | b
        else:
            w = buf[bpp * i + 3]
            pixel = (w << 24) | (r << 16) | (g << 8) | b
        ws.ws2811_led_set(channel, i, pixel)

    resp = ws.ws2811_render(_led_strip)
    if resp != ws.WS2811_SUCCESS:
        message = ws.ws2811_get_return_t_str(resp)
        raise RuntimeError(
            "ws2811_render failed with code {0} ({1})".format(resp, message)
        )
    time.sleep(0.001 * ((len(buf) // 100) + 1))  # about 1ms per 100 bytes


def neopixel_cleanup():
    """Cleanup when we're done"""
    global _led_strip

    if _led_strip is not None:
        # Ensure ws2811_fini is called before the program quits.
        ws.ws2811_fini(_led_strip)
        # Example of calling delete function to clean up structure memory.  Isn't
        # strictly necessary at the end of the program execution here, but is good practice.
        ws.delete_ws2811_t(_led_strip)
        _led_strip = None
