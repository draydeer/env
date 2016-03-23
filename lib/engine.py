

import storage

from lib.drivers.holder.holder import\
     Holder as DriverHolder
from lib.errors import\
     BadArgumentError
from lib.event_handlers.key_detach  import\
     KeyDetach
from lib.event_handlers.key_invalidate  import\
     KeyInvalidate
from packages.config import\
     Config


class Engine:

    _config = None
    _event_handlers = {}
    _storage = None

    def __init__(
        self, config=None
    ):
        self._config = Config(config)
        self._event_handlers = {
            'key.detach': KeyDetach(self),
            'key.invalidate': KeyInvalidate(self),
        }
        self._storage = storage.Storage(self)

    def get_config(
        self
    ):
        return self._config

    def get_driver_holder(
        self
    ):
        return DriverHolder

    def set_storage_mode(
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

    def set_storage_route(
        self, pattern, driver=None
    ):
        self._storage.set_route(pattern, driver)

        return self

    def event(
        self, event, *args
    ):
        return self._event_handlers[event](*args) if event in self._event_handlers else None

    def g(
        self, k, d=None, raw=False
    ):
        return self._storage.g(k, d, raw)
