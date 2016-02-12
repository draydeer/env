

import gevent
import re

from lib.drivers.factory.factory\
    import Factory as DriverFactory
from lib.errors\
    import ExistsError, NotExistsError
from lib.storage_route\
    import StorageRoute
from lib.storage_value\
    import StorageValue


class StorageTimer:

    _f = None
    _timers = {}

    def __init__(
        self
    ):
        pass

    def set_f(
        self, f
    ):
        self._f = f

        return self

    def attach(
        self, timeout, v, payload=None
    ):
        timeout = int(timeout)

        if timeout > 0:
            if self._timers.get(timeout) is None:
                def f():
                    while True:
                        gevent.sleep(timeout)

                        if self._f:
                            self._f(self._timers[timeout])

                self._timers[timeout] = {}

                gevent.spawn(f)

        self._timers[timeout][v] = payload

    def detach(
        self, v
    ):
        pass


class Storage:

    _active_driver = DriverFactory.get_default()
    _key_routes = {}
    _timer = StorageTimer()
    _values = {}

    def _as_client(
        self, context
    ):
        for k, v in context.iteritems():
            if k in self._values:
                self._values[k].update()

    def _as_keeper(
        self, context
    ):
        for k, v in context.iteritems():
            if k in self._values:
                self._values[k].update()

    def _as_server(
        self, context
    ):
        for k, v in context.iteritems():
            if k in self._values:
                self._values.pop(k)

    def __init__(
        self
    ):
        self.set_route('.*')

        self.set_mode_keeper()

    def set_active_driver(
        self, driver, config=None
    ):
        self._active_driver = DriverFactory(driver, config) if isinstance(driver, str) else driver

        return self

    def set_mode_client(
        self
    ):
        self._timer.set_f(self._as_client)

        return self.set_active_driver('env')

    def set_mode_keeper(
        self
    ):
        self._timer.set_f(self._as_keeper)

        return self

    def set_mode_server(
        self
    ):
        self._timer.set_f(self._as_server)

        return self

    def set_route(
        self, pattern
    ):
        self._key_routes[re.compile(pattern)] = StorageRoute(self._active_driver)

        return self

    def g(
        self, k, d=None
    ):
        d = k.split(':')

        if len(d):
            k = d[0].split('.')

            if len(k):
                if k[0] not in self._values:
                    index = reduce(lambda x, y: y if y.search(k[0]) else x, self._key_routes.iterkeys(), None)

                    if index is not None:
                        self._values[k[0]] = StorageValue(k[0], self._key_routes[index].driver, self._timer, decryption_key=d[1] if 2 in d else None, sync_each=d[1] if 1 in d else 30)
                    else:
                        return NotExistsError()

                return self._values[k[0]].g(k[1:])

        return NotExistsError()
