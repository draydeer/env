

class IncompatibleError(BaseException):
    pass


def cast(
    v, t
):
    if isinstance(v, t):
        return v

    raise IncompatibleError(v.__class__.__name__ + ' is not an instance of ' + v.__class__.__name__)


cast = cast
