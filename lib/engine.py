

import storage


class Engine:

    _storage = None

    def __init__(
        self
    ):
        self._storage = storage.Storage()

    def g(
        self, k, d=None
    ):
        return self._storage.g(k, d)
