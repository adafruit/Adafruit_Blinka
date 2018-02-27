from adafruit_blinka import agnostic

if agnostic.microcontroller == "esp8266":
    from adafruit_blinka.microcontroller.esp8266.pin import *
elif agnostic.microcontroller == "stm32":
    from adafruit_blinka.microcontroller.stm32.pin import *
else:
    raise NotImplementedError("Microcontroller not supported")