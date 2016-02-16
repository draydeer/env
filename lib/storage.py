

import gevent
import re

from lib.errors\
    import BadArgumentError, NotExistsError
from lib.storage_compiler\
    import StorageCompiler
from lib.storage_route\
    import StorageRoute
from lib.storage_key\
    import StorageKey


class StorageRefreshTimer:

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
        self, timeout, k, payload=None
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

            self._timers[timeout][k] = payload

    def detach(
        self, v
    ):
        pass


class Storage:

    _active_driver = None
    _compiler = None
    _engine = None
    _key_routes = {}
    _timer = StorageRefreshTimer()
    _values = {}

    def _on_detach(
        self, context
    ):
        for k, v in context.iteritems():
            if k in self._values:
                self._engine.event('detached', self._values.pop(k))

    def _on_invalidate(
        self, context
    ):
        for k, v in context.iteritems():
            if k in self._values:
                self._values[k].set_value(self._compiler.compile(k, self._values[k].update().get_value())).invalidate()

    def __init__(
        self, engine
    ):
        self._engine = engine

        self.set_mode_keeper()

    def set_active_driver(
        self, driver, config=None
    ):
        self._active_driver = self._engine.get_driver_factory().req(driver, config) if isinstance(driver, str) else driver

        return self

    def set_route(
        self, pattern
    ):
        self._key_routes[pattern] = [re.compile(pattern), StorageRoute(self._active_driver)]

        return self

    def set_mode_client(
        self
    ):
        self._compiler = None

        self._timer.set_f(self._on_invalidate)

        return self.set_active_driver('env')

    def set_mode_keeper(
        self
    ):
        self._compiler = StorageCompiler(self._engine, self)

        self._timer.set_f(self._on_invalidate)

        return self.set_active_driver(self._engine.get_driver_factory().get_default())

    def set_mode_server(
        self
    ):
        self._compiler = StorageCompiler(self._engine, self)

        self._timer.set_f(self._on_detach)

        return self

    def g(
        self, k, d=None, raw=False
    ):
        k = k.split(':')

        decryption_key = k[2] if len(k) > 2 else None
        sync_period = k[1] if len(k) > 1 else None

        if len(k[0]):
            k = k[0].split('.')

            if len(k):
                if k[0] not in self._values:
                    if len(self._key_routes) == 0:
                        self.set_route('.*')

                    route = self._key_routes.get(
                        reduce(lambda x, (a, b): a if b[0].search(k[0]) else x, self._key_routes.iteritems(), None)
                    )

                    if route is not None:
                        (regex, route) = route

                        storage_key = StorageKey(self._engine, k[0], route.driver, decryption_key=decryption_key)

                        if self._compiler:
                            storage_key.set_value(self._compiler.compile(k[0], storage_key.get_value()))

                        if sync_period:
                            if sync_period.isdigit():
                                self._timer.attach(sync_period, k[0])
                            else:
                                raise BadArgumentError('invalid sync period')
                        else:
                            self._timer.attach(60, k[0])

                        self._values[k[0]] = storage_key.invalidate()
                    else:
                        raise NotExistsError('route not found')

                return self._values[k[0]].to_dict() if raw else self._values[k[0]].g(k[1:], d)

        raise BadArgumentError()
