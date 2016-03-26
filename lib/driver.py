

from lib.configurable import\
    Configurable
from packages.serializer import\
     Dict


class Driver(Configurable):

    _client = None

    def __init__(
        self, config=None
    ):
        Configurable.__init__(self, config)

    def g(
        self, k
    ):
        return None


class Value(Dict):

    data = None
    type = None

    def __init__(
        self, data=None, type=None
    ):
        self.data = data
        self.type = type
