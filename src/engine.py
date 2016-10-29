
import configurable
import const
import time

from src.cryptors.holder.holder import Holder as CryptorsHolder
from src.drivers.holder.holder import Holder as DriverHolder
from src.errors import BadArgumentError
from src.event_handlers.key_detach import KeyDetach
from src.event_handlers.key_invalidate import KeyInvalidate
from src.society import Society
from src.storage import Storage
from packages.logger import logger


class Engine(configurable.Configurable):

    VERSION = 1.0

    _event_handlers = {}
    _society = None
    _storage = None
    _time_start = None

    def __init__(self, config=None):
        configurable.Configurable.__init__(self, config)

        self._event_handlers = {'key.detach': KeyDetach(self), 'key.invalidate': KeyInvalidate(self)}
        self._society = Society(
            self,
            self.config.g('society.members', []),
            self.config.g('society.announceInterval', 60)
        )
        self._storage = Storage(self)
        self._time_start = time.time()

    @property
    def alive(self):
        return True

    @property
    def client_id(self):
        return self._config.get('clientId')

    @property
    def cryptors_holder(self):
        return CryptorsHolder

    @property
    def driver_holder(self):
        return DriverHolder

    @property
    def logger(self):
        return logger

    @property
    def mode(self):
        return logger

    @property
    def society(self):
        return self._society

    @property
    def storage(self):
        return self._storage

    @property
    def time_start(self):
        return self._time_start

    @property
    def version(self):
        return Engine.VERSION

    def set_storage_mode(self, value):
        if value == 'client':
            self._storage.set_mode_client()

            return self

        if value == 'keeper':
            self._storage.set_mode_keeper()

            return self

        if value == 'server':
            self._storage.set_mode_server()

            return self

        raise BadArgumentError('Unknown mode.')

    def set_storage_route(self, pattern, driver=None):
        self._storage.set_route(pattern, driver)

        return self

    def set_member_port(self, value=const.PORT):
        self._society.set_port(value)

        return self

    def event(self, event, *args):
        return self._event_handlers[event](*args) if event in self._event_handlers else None

    def g(self, k, d=None, raw=False):
        return self._storage.g(k, d, raw)
