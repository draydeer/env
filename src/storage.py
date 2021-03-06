
import gevent
import re

from src.errors import BadArgumentError, NotExistsError
from engine_module import EngineModule
from src.storage_compiler import StorageCompiler
from src.storage_route import StorageRoute
from src.storage_root_key import StorageRootKey
from packages.cast import try_type
from packages.logger import logger


class StorageRefreshTimer:

    _refresh_callback = None
    _timer_payloads_by_intervals = {}

    def __init__(self):
        pass

    def set_f(self, refresh_callback):
        self._refresh_callback = refresh_callback

        return self

    def attach(self, interval, k, payload=None):
        interval = int(interval)

        if interval > 0:
            if interval not in self._timer_payloads_by_intervals:
                def f():
                    while True:
                        gevent.sleep(interval)

                        if self._refresh_callback:
                            self._refresh_callback(self._timer_payloads_by_intervals[interval])

                self._timer_payloads_by_intervals[interval] = {}

                gevent.spawn(f)

            self._timer_payloads_by_intervals[interval][k] = payload

    def detach(self, v):
        pass


class Storage(EngineModule):

    DEFAULT_ROUTE_PATTERN = '.*'

    _active_driver = None
    _allowed_rules = {}
    _compiler = None
    _engine = None
    _keys = {}
    _key_routes = {}
    _timer = StorageRefreshTimer()

    def _on_detach(self, keys):
        patch = []
        total = 0

        for k in list(keys.keys()):
            if k in self._keys:
                self._engine.event('key.detach', self._keys.pop(k))

                total += 1
            else:
                patch.append(k)

        map(keys.pop, patch)

        logger.info("Keys pruned: %s" % total)

    def _on_invalidate(self, keys):
        patch = []
        total = 0

        for k in list(keys.keys()):
            if k in self._keys:
                self._keys[k].set_value(
                    self._keys[k].update().get_value()
                ).invalidate()

                total += 1
            else:
                patch.append(k)

        map(keys.pop, patch)

        logger.info("Keys updated: %s" % total)

    def _on_invalidate_compile(self, keys):
        patch = []
        total = 0

        for k in list(keys.keys()):
            if k in self._keys:
                self._keys[k].set_value(
                    self._compiler.compile(k, self._keys[k].update().get_value())
                ).invalidate()

                total += 1
            else:
                patch.append(k)

        map(keys.pop, patch)

        logger.info("Keys updated: %s" % total)

    def __init__(self, engine):
        EngineModule.__init__(self, engine)

        self.set_mode_keeper().set_route(Storage.DEFAULT_ROUTE_PATTERN)

        # preset routes
        for k, v in engine.config.g('routes', {}).iteritems():
            self.set_route(k, v.get('driver'), v.get('projection')) if isinstance(v, dict) else self.set_route(k, v)

        # preset keys
        for i, k in enumerate(engine.config.g('keys', [])):
            try:
                self.g(k)
            except BaseException as e:
                logger.error(e)

    def set_active_driver(self, driver, config=None):
        if isinstance(driver, str):
            self._active_driver = self._engine.driver_holder.req(driver, self._engine, config)
        else:
            self._active_driver = driver

        return self

    def set_compiler(self, compiler):
        self._compiler = try_type(compiler, StorageCompiler, None)

        return self

    def set_route(self, pattern, driver=None, projection=None):
        self._key_routes[pattern] = [
            re.compile(pattern),
            StorageRoute(
                self._engine.driver_holder.req(driver, self._engine) if driver else self._active_driver,
                projection
            )
        ]

        return self

    def set_mode_client(self):
        self.set_compiler(None)._timer.set_f(self._on_invalidate)

        self._allowed_rules = {'var': True}

        return self.set_active_driver('env')

    def set_mode_keeper(self):
        self.set_compiler(StorageCompiler(self._engine, self))._timer.set_f(self._on_invalidate_compile)

        self._allowed_rules = {'env': True, 'var': True}

        return self.set_active_driver(self._engine.driver_holder.get_default(self._engine))

    def set_mode_server(self):
        self.set_compiler(StorageCompiler(self._engine, self))._timer.set_f(self._on_detach)

        self._allowed_rules = {'env': True}

        return self

    def g(self, path, default_value=None, raw=False):
        path = path.split(':')

        decryption_key = path[2] if len(path) > 2 else None
        decryptor = path[3] if len(path) > 3 else None
        sync_period = path[1] if len(path) > 1 else None

        if len(path[0]):
            path = path[0].split('.')

            if len(path):
                if path[0] not in self._keys:
                    route = reduce(
                        lambda x, (a, b): b if a != Storage.DEFAULT_ROUTE_PATTERN and b[0].match(path[0]) else x,
                        self._key_routes.iteritems(),
                        None
                    )

                    if route is None:
                        route = self._key_routes.get(Storage.DEFAULT_ROUTE_PATTERN)

                    if route is not None:
                        (regex, route) = route

                        if sync_period:
                            if sync_period.isdigit():
                                self._timer.attach(sync_period, path[0])
                            else:
                                raise BadArgumentError('Invalid sync period.')
                        else:
                            self._timer.attach(60, path[0])

                        storage_key = StorageRootKey(
                            self._engine,
                            route.projection or path[0],
                            route.driver,
                            decryption_key=decryption_key
                        )

                        if self._compiler:
                            storage_key.set_value(self._compiler.compile(
                                path[0],
                                storage_key.value,
                                self._allowed_rules
                            ))

                        self._keys[path[0]] = storage_key.invalidate()
                    else:
                        raise NotExistsError('Route not found.')

                if raw:
                    self._keys[path[0]].to_dict()

                return self._keys[path[0]].g(path[1:], default_value, decryption_key, decryptor)

        raise BadArgumentError()
