class Enum(object):


    @classmethod
    def iteritems(cls):
        for key in dir(cls):
            val = getattr(cls, key)
            if type(val) is cls:
                yield (key, val)


    def __repr__(self):
        """
        Assumes instance will be found as attribute of own
        class. Returns dot-subscripted path to instance
        """
        cls = type(self)
        for key in dir(cls):
            if getattr(cls, key) is self:
                return "{}.{}.{}".format(cls.__module__, cls.__qualname__, key)
        return repr(self)