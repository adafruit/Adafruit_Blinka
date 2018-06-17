# Pins dont exist in CPython so...lets make our own!
class Pin:
    def __init__(self, name, bcm_number):
        self._name = name
        self._number = bcm_number

SDA = Pin("SDA", 2)
SCL = Pin("SCL", 3)
D4 = Pin("BCM 4", 4)
D17 = Pin("BCM 17", 17)
D18 = Pin("BCM 18", 18)

# TODO: more here...
