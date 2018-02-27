from adafruit_blinka.agnostic import microcontroller

if microcontroller == "esp8266":
    pin_count = 10
elif microcontroller == "samd21":
    pin_count = 38
else:
    raise NotImplementedError("Microcontroller not supported")
