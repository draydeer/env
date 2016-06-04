

class Error(BaseException):

    message = None

    @classmethod
    def throw(cls, value=None):
        raise cls(value)


class BadArgumentError(Error):
    pass


class CircularReferenceError(Error):
    pass


class ConflictError(Error):
    pass


class ExistsError(Error):
    pass


class InternalError(Error):
    pass


class NotExistsError(Error):
    pass
