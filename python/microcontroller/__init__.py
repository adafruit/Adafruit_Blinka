import agnostic
if agnostic.platform == "esp8266":
    from microcontroller.esp8266 import *