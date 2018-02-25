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


class ContextManaged:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()

class Lockable(ContextManaged):
    _locked = False

    def try_lock(self):
        if self._locked:
            return False
        else:
            self._locked=True
            return True

    def unlock(self):
        if self._locked:
            self._locked = False
        else:
            raise ValueError("Not locked")
