

import storage

from lib.drivers.holder.holder\
    import Holder as DriverHolder
from lib.errors\
    import BadArgumentError
from lib.types.system_file\
    import SystemFile


class Engine:

    _storage = None

    handlers = {}

    def __init__(
        self
    ):
        self._storage = storage.Storage(self)

        self.handlers = {
            'system.file': SystemFile(self),
        }

    def g(
        self, k, d=None, raw=False
    ):
        return self._storage.g(k, d, raw)

    def get_driver_factory(
        self
    ):
        return DriverHolder

    def set_mode(
        self, value
    ):
        if value == 'client':
            self._storage.set_mode_client()

            return self

        if value == 'keeper':
            self._storage.set_mode_keeper()

            return self

        if value == 'server':
            self._storage.set_mode_server()

            return self

        raise BadArgumentError('unknown mode')

    def event(
        self, event, value
    ):
        handler = self.handlers.get(value.get_type())

        if handler:
            value = value.get_value()

            if isinstance(value, dict):
                return handler(**value)

            if isinstance(value, list):
                return handler(*value)

        return None
