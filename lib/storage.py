

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
from packages.cast\
    import try_type


class StorageRefreshTimer:

    _f = None
    _timer_payloads_by_intervals = {}

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
        self, interval, k, payload=None
    ):
        interval = int(interval)

        if interval > 0:
            if interval not in self._timer_payloads_by_intervals:
                def f():
                    while True:
                        gevent.sleep(interval)

                        if self._f:
                            self._f(self._timer_payloads_by_intervals[interval])

                self._timer_payloads_by_intervals[interval] = {}

                gevent.spawn(f)

            self._timer_payloads_by_intervals[interval][k] = payload

    def detach(
        self, v
    ):
        pass


class Storage:

    DEFAULT_ROUTE_PATTERN = '.*'

    _active_driver = None
    _compiler = None
    _engine = None
    _keys = {}
    _key_routes = {}
    _timer = StorageRefreshTimer()

    def _on_detach(
        self, keys
    ):
        patch = []

        for k in list(keys.keys()):
            if k in self._keys:
                self._engine.event('key.detach', self._keys.pop(k))
            else:
                patch.append(k)

        map(keys.pop, patch)

    def _on_invalidate(
        self, keys
    ):
        patch = []

        for k in list(keys.keys()):
            if k in self._keys:
                self._keys[k].set_value(self._keys[k].update().get_value()).invalidate()
            else:
                patch.append(k)

        map(keys.pop, patch)

    def _on_invalidate_compile(
        self, keys
    ):
        patch = []

        for k in list(keys.keys()):
            if k in self._keys:
                self._keys[k].set_value(self._compiler.compile(k, self._keys[k].update().get_value())).invalidate()
            else:
                patch.append(k)

        map(keys.pop, patch)

    def __init__(
        self, engine
    ):
        self._engine = engine

        self.set_mode_keeper().set_route(Storage.DEFAULT_ROUTE_PATTERN)

        # preset routes
        for k, v in engine.get_config().g('routes', {}).iteritems():
            self.set_route(k, v)

        # preset keys
        for i, k in enumerate(engine.get_config().g('keys', [])):
            self.g(k)

    def set_active_driver(
        self, driver, config=None
    ):
        self._active_driver = self._engine.get_driver_holder().req(driver, config) if isinstance(driver, str) else driver

        return self

    def set_compiler(
        self, compiler
    ):
        self._compiler = try_type(compiler, StorageCompiler, None)

        return self

    def set_route(
        self, pattern, driver=None
    ):
        self._key_routes[pattern] = [re.compile(pattern), StorageRoute(self._engine.get_driver_holder().req(driver) if driver else self._active_driver)]

        return self

    def set_mode_client(
        self
    ):
        self.set_compiler(None)._timer.set_f(self._on_invalidate)

        return self.set_active_driver('env')

    def set_mode_keeper(
        self
    ):
        self.set_compiler(StorageCompiler(self._engine, self))._timer.set_f(self._on_invalidate_compile)

        return self.set_active_driver(self._engine.get_driver_holder().get_default())

    def set_mode_server(
        self
    ):
        self.set_compiler(StorageCompiler(self._engine, self))._timer.set_f(self._on_detach)

        return self

    def g(
        self, k, default_value=None, raw=False
    ):
        k = k.split(':')

        decryption_key = k[2] if len(k) > 2 else None
        sync_period = k[1] if len(k) > 1 else None

        if len(k[0]):
            k = k[0].split('.')

            if len(k):
                if k[0] not in self._keys:
                    route = reduce(
                        lambda x, (a, b): b if a != Storage.DEFAULT_ROUTE_PATTERN and b[0].match(k[0]) else x,
                        self._key_routes.iteritems(),
                        None
                    )

                    if route is None:
                        route = self._key_routes.get(Storage.DEFAULT_ROUTE_PATTERN)

                    if route is not None:
                        (regex, route) = route

                        if sync_period:
                            if sync_period.isdigit():
                                self._timer.attach(sync_period, k[0])
                            else:
                                raise BadArgumentError('invalid sync period')
                        else:
                            self._timer.attach(60, k[0])

                        storage_key = StorageKey(self._engine, k[0], route.driver, decryption_key=decryption_key)

                        if self._compiler:
                            storage_key.set_value(self._compiler.compile(k[0], storage_key.get_value()))

                        self._keys[k[0]] = storage_key.invalidate()
                    else:
                        raise NotExistsError('route not found')

                return self._keys[k[0]].to_dict() if raw else self._keys[k[0]].g(k[1:], default_value)

        raise BadArgumentError()
