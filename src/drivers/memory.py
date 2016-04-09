

from src.driver import Driver
from src.errors import NotExistsError


class Memory(Driver):

    _values = {}

    def _on_init(
        self
    ):
        if isinstance(self._config['values'], dict):
            self._values = self._config['values']

    def g(
        self, k
    ):
        if k in self._values:
            return self._values[k]

        raise NotExistsError(k)
