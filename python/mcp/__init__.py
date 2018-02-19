"""Module providing runtime utility objects to support the Micro/CircuitPython api"""

class Enum(object):
    """
        Object supporting CircuitPython-style of static symbols
        as seen with Direction.OUTPUT, Pull.UP
    """

    def __repr__(self):
        """
        Assumes instance will be found as attribute of own class.
        Returns dot-subscripted path to instance
        (assuming absolute import of containing package)
        """
        cls = type(self)
        for key in dir(cls):
            if getattr(cls, key) is self:
                return "{}.{}.{}".format(cls.__module__, cls.__qualname__, key)
        return repr(self)

    @classmethod
    def iteritems(cls):
        """
            Inspects attributes of the class for instances of the class
            and returns as key,value pairs mirroring dict#iteritems
        """
        for key in dir(cls):
            val = getattr(cls, key)
            if type(val) is cls:
                yield (key, val)


class Pin(Enum):
    def __init__(self, id):
        """ id type is likely platform-specific"""
        self.id = id
    pass
