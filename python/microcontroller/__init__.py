import agnostic

if agnostic.microcontroller == "esp8266":
    from microcontroller.esp8266 import pin
elif agnostic.microcontroller == "stm32":
    from microcontroller.stm32 import pin
