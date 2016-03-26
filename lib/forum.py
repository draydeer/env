

import gevent
import requests

from lib.engine_module import\
    EngineModule
from random import\
    sample


class ServerDescriptor:

    servers = []
    version = 0

    def __init__(
        self, servers, version
    ):
        self.servers = servers if isinstance(servers, list) else []
        self.version = version


class Forum(EngineModule):

    _announce_interval = 60
    _servers = {}

    def _announce_loop(
        self
    ):
        while self.alive:
            self.announce()

            gevent.sleep(self._announce_interval)

    def __init__(
        self, engine, servers, announce_interval=60
    ):
        EngineModule.__init__(self, engine)

        self._announce_interval = announce_interval if announce_interval >= 15 else 15
        self._servers = {k: None for k in (servers if isinstance(servers, list) else [])}

        gevent.spawn(self._announce_loop)

    def announce(
        self
    ):
        patch = {}

        for k, v in self._servers.iteritems():
            result = None

            try:
                result = requests.request(
                    'INFO',
                    k,
                    json={
                        'servers': [server for server in filter(lambda x: x != k, self._servers.iterkeys())],
                        'version': self._engine.version,
                    },
                    params={
                        'clientId': self._engine.client_id,
                    }
                )

                if result.status_code == 200:
                    result = result.json()

                    patch[k] = ServerDescriptor(**(result if isinstance(result, dict) else {}))
                else:
                    result = None

                    self.logger.critical('Server detached: ' + k + ' (code: ' + result.status_code + ')')
            except requests.exceptions.ConnectionError:
                self.logger.critical('Server detached: ' + k + ' (connection timeout)')

            if result is None:
                patch[k] = None

                self.event('on_server_detach', k)

        for k, v in patch.iteritems():
            if v is None:
                self._servers.pop(k)
            else:
                self._servers[k] = v

        return self

    def attach(
        self, k, environment=None
    ):
        self._servers[k] = ServerDescriptor(**(environment if isinstance(environment, dict) else {}))

        return self

    def detach(
        self, k
    ):
        self._servers.pop(k)

        return self

    def select(
        self
    ):
        k = sample(self._servers, 1)[0]

        return k
