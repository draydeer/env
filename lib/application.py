

import json
import traceback

from gevent.pywsgi import\
     WSGIServer
from lib.engine import\
     Engine
from lib.errors import\
     Error
from packages.config import\
     Config
from packages.logger import\
     logger


class Application:

    _arguments = None
    _config = None
    _engine = None
    _errors = {
        'BadArgumentError': '400 Bag Request',
        'CircularReferenceError': '409 Conflict',
        'ConflictError': '409 Conflict',
        'NotExistsError': '404 Not Found',
    }

    def _as_none(
        self, value
    ):
        return None if value == '' else value

    def _on_route_delete(
        self, path
    ):
        return None

    def _on_route_get(
        self, path
    ):
        return self._engine.g(path)

    def _on_route_info(
        self, path
    ):
        return self._engine.g(path, None, True)

    def _on_route_patch(
        self, path
    ):
        return None

    def _on_route_post(
        self, pattern, driver=None
    ):
        self._engine.set_storage_route(pattern, self._as_none(driver))

    def _on_route_put(
        self
    ):
        return None

    def __init__(
        self, args, config=None
    ):
        self._arguments = args
        self._config = Config(config)
        self._engine = Engine(self._config).set_storage_mode(args.arg(['client', 'keeper', 'server'], 'client'))

    def run(
        self
    ):
        logger\
            .splitter()\
            .indented('Envd, version 0.1a')\
            .splitter()\
            .info('Mode: ' + self._arguments.arg(['client', 'keeper', 'server'], 'client'))

        routes = {
            'DELETE': [
                self._on_route_delete,
                1
            ],
            'GET': [
                self._on_route_get,
                1
            ],
            'INFO': [
                self._on_route_info,
                1
            ],
            'PATCH': [
                self._on_route_patch,
                1
            ],
            'POST': [
                self._on_route_post,
                1
            ],
            'PUT': [
                self._on_route_put,
                1
            ]
        }

        def f_resp(
            env, start_response
        ):
            route = routes.get(env['REQUEST_METHOD'])

            if route:
                try:
                    data = env['PATH_INFO'][1:].split('/')

                    if len(data) >= route[1]:
                        code = '200 OK'
                        data = route[0](*data)
                    else:
                        code = self._errors['BadArgumentError']
                        data = None
                except BaseException as e:
                    code = self._errors[e.__class__.__name__] if e.__class__.__name__ in self._errors else '500 Internal Server Error'
                    data = e.message if isinstance(e, Error) else None

                    if self._arguments.debug:
                        traceback.print_exc()
            else:
                code = self._errors['NotExistsError']
                data = None

            start_response(
                code,
                [('Content-Type', 'application/json')]
            )

            return [json.dumps(data)]

        bind = self._arguments.arg('bind', '127.0.0.1')
        port = int(self._arguments.arg(['p', 'port'], 8088))

        logger.warning('Server is up and running on: ' + bind + ':' + str(port))

        WSGIServer(
            (bind, port),
            f_resp,
            log=None
        ).serve_forever()
