import agnostic

if agnostic.platform == "esp8266":
    from microcontroller.esp8266 import pin
elif agnostic.platform == "stm32":
    from microcontroller.stm32 import pin
