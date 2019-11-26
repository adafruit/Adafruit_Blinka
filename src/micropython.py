def const(x):
    return x


def native(f):
    return f


def viper(f):
    raise SyntaxError("invalid micropython decorator")


def asm_thumb(f):
    raise SyntaxError("invalid micropython decorator")