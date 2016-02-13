

class Error(BaseException):

    @classmethod
    def throw(
        cls, value=None
    ):
        raise cls(value)


class CyclicReferenceError(Error):
    pass


class BadArgumentError(Error):
    pass


class ExistsError(Error):
    pass


class NotExistsError(Error):
    pass
