

import gevent
import re
import os

from lib.errors\
    import BadArgumentError, CyclicReferenceError, NotExistsError
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
    _engine = None
    _key_routes = {}
    _on_value_recompile = None
    _timer = StorageRefreshTimer()
    _values = {}

    def _get_value_recompiled(
        self, value, k=None, locks=None
    ):
        if locks is None:
            locks = {}

        if isinstance(value, dict) and value.get('@@'):
            other = self.g(value.get('@@'), locks=locks)

            if isinstance(other, dict):
                other.update(value)

                value = other

                value.pop('@@')

        iter = value.iteritems() if isinstance(value, dict) else enumerate(value) if isinstance(value, list) else None

        if iter:
            replacement = {}

            for k, v in iter:
                if (isinstance(v, str) or isinstance(v, unicode)) and v[0:2] == '@@':
                    path = v.split(':')

                    if len(path) > 2:
                        if path[1] == 'env':
                            replacement[k] = self.g(path[2], locks=locks)

                            continue

                        if path[1] == 'sys':
                            replacement[k] = os.environ.get(path[2])

                            continue

                if isinstance(v, dict) or isinstance(v, list):
                    replacement[k] = self._get_value_recompiled(v, locks=locks)

            if isinstance(value, dict):
                value.update(replacement)
            elif isinstance(value, list):
                value = [replacement[i] if i in replacement else v for i, v in enumerate(value)]

        return value

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
                self._values[k].set_value(self._on_value_recompile(self._values[k].update().get_value())).invalidate()

    def __init__(
        self, engine
    ):
        self._engine = engine

        self.set_mode_keeper()

    def set_active_driver(
        self, driver, config=None
    ):
        self._active_driver = self._engine.get_driver_factory().produce(driver, config) if isinstance(driver, str) else driver

        return self

    def set_route(
        self, pattern
    ):
        self._key_routes[pattern] = [re.compile(pattern), StorageRoute(self._active_driver)]

        return self

    def set_mode_client(
        self
    ):
        self._on_value_recompile = None

        self._timer.set_f(self._on_invalidate)

        return self.set_active_driver('env')

    def set_mode_keeper(
        self
    ):
        self._on_value_recompile = self._get_value_recompiled

        self._timer.set_f(self._on_invalidate)

        return self.set_active_driver(self._engine.get_driver_factory().get_default())

    def set_mode_server(
        self
    ):
        self._on_value_recompile = self._get_value_recompiled

        self._timer.set_f(self._on_detach)

        return self

    def g(
        self, k, d=None, raw=False, locks=None
    ):
        k = k.split(':')

        decryption_key = k[2] if len(k) > 2 else None
        sync_period = k[1] if len(k) > 1 else None

        if len(k[0]):
            k = k[0].split('.')

            if len(k):
                if k[0] not in self._values:

                    """ capture update lock for key """
                    if locks:
                        if locks.get(k[0]):
                            raise CyclicReferenceError(k[0])
                        else:
                            locks[k[0]] = True

                    if len(self._key_routes) == 0:
                        self.set_route('.*')

                    route = self._key_routes.get(reduce(lambda x, (a, b): a if b[0].search(k[0]) else x, self._key_routes.iteritems(), None))

                    try:
                        if route is not None:
                            (regex, route) = route

                            self._values[k[0]] = StorageKey(self._engine, k[0], route.driver, decryption_key=decryption_key)

                            if self._on_value_recompile:
                                self._values[k[0]].set_value(self._on_value_recompile(self._values[k[0]].get_value(), locks))

                            self._values[k[0]].invalidate()

                            if sync_period:
                                if sync_period.isdigit():
                                    self._timer.attach(sync_period, k[0])
                                else:
                                    raise BadArgumentError('invalid sync period')
                            else:
                                self._timer.attach(60, k[0])
                        else:
                            raise NotExistsError('route not found')
                    except BaseException as e:
                        if locks:
                            locks.pop(k[0])

                        raise e

                    """ release update lock for key """
                    if locks:
                        locks.pop(k[0])

                return self._values[k[0]].to_dict() if raw else self._values[k[0]].g(k[1:], d)

        raise BadArgumentError()
