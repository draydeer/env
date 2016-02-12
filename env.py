

import json

from gevent.pywsgi\
    import WSGIServer
from gevent\
    import monkey


monkey.patch_all()


from config.active\
    import config
from lib.engine\
    import Engine



monkey.patch_thread()
monkey.patch_all()




engine = Engine()


def application(
    env, start_response
):
    try:
        start_response(
            '200 OK',
            [('Content-Type', 'application/json')]
        )

        return [json.dumps(engine.g(env['PATH_INFO'][1:]))]
    except BaseException as e:
        start_response(
            '404 Not Found',
            [('Content-Type', 'application/json')]
        )

        return [b'null']


if __name__ == '__main__':
    WSGIServer(('', 8088), application).serve_forever()
