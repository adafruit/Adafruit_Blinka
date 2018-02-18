def create_pin():
    from microcontroller import Pin
    name, pin = next(Pin.iteritems())  # grab first pin
    return pin

def create_dio():
    import digitalio
    return digitalio.DigitalInOut(create_pin())