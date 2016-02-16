

import traceback

from gevent.pywsgi\
    import WSGIServer
from gevent\
    import monkey


monkey.patch_all()


import json
import sys

from lib.engine\
    import Engine
from lib.errors\
    import Error
from packages.args\
    import Args


monkey.patch_all()


args = Args.parse(sys.argv)
engine = Engine().set_mode(args.arg(['m', 'mode'], 'client'))
errors = {
    'BadArgumentError': '400 Bag Request',
    'CircularReferenceError': '409 Conflict',
    'NotExistsError': '404 Not Found',
}


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
            errors[e.__class__.__name__] if e.__class__.__name__ in errors else '500 Internal Server Error',
            [('Content-Type', 'application/json')]
        )

        return [json.dumps(e.message) if isinstance(e, Error) else 'null']


WSGIServer(('', int(args.arg(['p', 'port'], 8088))), application).serve_forever()
