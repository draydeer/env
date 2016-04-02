

import configurable
import const
import time

from lib.drivers.holder.holder import\
    Holder as DriverHolder
from lib.errors import\
    BadArgumentError
from lib.event_handlers.key_detach import\
    KeyDetach
from lib.event_handlers.key_invalidate import\
    KeyInvalidate
from lib.socium import\
    Socium
from lib.storage import\
    Storage
from packages.logger import\
    logger


class Engine(configurable.Configurable):

    VERSION = 1.0

    _event_handlers = {}
    _socium = None
    _storage = None
    _time_start = None

    def __init__(
        self, config=None
    ):
        configurable.Configurable.__init__(self, config)

        self._event_handlers = {'key.detach': KeyDetach(self), 'key.invalidate': KeyInvalidate(self)}
        self._socium = Socium(self, self.config.g('socium.members', []), self.config.g('socium.announceInterval', 60))
        self._storage = Storage(self)
        self._time_start = time.time()

    @property
    def alive(
        self
    ):
        return True

    @property
    def client_id(
        self
    ):
        return self._config.get('clientId')

    @property
    def logger(
        self
    ):
        return logger

    @property
    def mode(
        self
    ):
        return logger

    @property
    def socium(
        self
    ):
        return self._socium

    @property
    def storage(
        self
    ):
        return self._storage

    @property
    def time_start(
        self
    ):
        return self._time_start

    @property
    def version(
        self
    ):
        return Engine.VERSION

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

    def set_member_port(
        self, value=const.PORT
    ):
        self._socium.set_port(value)

        return self

    def event(
        self, event, *args
    ):
        return self._event_handlers[event](*args) if event in self._event_handlers else None

    def g(
        self, k, d=None, raw=False
    ):
        return self._storage.g(k, d, raw)
