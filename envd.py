

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
        start_response(
            '500 Internal Server Error',
            [('Content-Type', 'application/json')]
        )

        raise e

        return [b'null']


WSGIServer(('', int(args.arg(['p', 'port'], 8088))), application).serve_forever()
