
class IncompatibleError(BaseException):
    pass


def try_type(v, *args):
    if reduce(lambda x, y: x or y, map(lambda x: v is None if x is None else isinstance(v, x), args)):
        return v

    raise IncompatibleError(
        v.__class__.__name__ + ' is not an instance of: ' + ' | '.join(map(lambda x: x.__class__.__name__, v))
    )


try_type = try_type
