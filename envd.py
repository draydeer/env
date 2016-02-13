

from gevent.pywsgi\
    import WSGIServer
from gevent\
    import monkey


monkey.patch_all()


import json
import sys

from config.active\
    import config
from lib.engine\
    import Engine
from lib.errors\
    import BadArgumentError, NotExistsError
from packages.args\
    import Args


monkey.patch_all()


args = Args.parse(sys.argv)
engine = Engine().set_mode(args.arg(['m', 'mode'], 'client'))


def application(
    env, start_response
):
    path = env['PATH_INFO'][1:].split('/')

    try:
        start_response(
            '200 OK',
            [('Content-Type', 'application/json')]
        )

        return [json.dumps(engine.g(path[0], None, len(path) > 1 and path[1] == '$'))]
    except BaseException as e:
        if isinstance(e, BadArgumentError):
            start_response(
                '400 Bag Request',
                [('Content-Type', 'application/json')]
            )

            return [json.dumps(e.message)]

        if isinstance(e, NotExistsError):
            start_response(
                '404 Not Found',
                [('Content-Type', 'application/json')]
            )

            return [json.dumps(e.message)]

        start_response(
            '500 Internal Server Error',
            [('Content-Type', 'application/json')]
        )

        return []


WSGIServer(('', int(args.arg(['p', 'port'], 8088))), application).serve_forever()
