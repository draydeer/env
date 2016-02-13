

from packages.serializer\
    import Dict


class Driver:

    _client = None
    _config = None

    def _on_init(
        self
    ):
        pass

    def __init__(
        self, config
    ):
        self._config = config

        self._on_init()

    def g(
        self, k
    ):
        return None


class Value(Dict):

    type = None
    v = None

    def __init__(
        self, v=None, type=None
    ):
        self.type = type
        self.v = v
