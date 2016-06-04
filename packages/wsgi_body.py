

import json


class WsgiBody:

    @classmethod
    def read(cls, env):
        try:
            length = int(env.get('CONTENT_LENGTH'))

            if length is not None:
                length = int(length)
        except:
            raise BaseException('incorrect request length')

        if length is not None:
            data = env['wsgi.input'].read(length)
        else:
            return ''

        content_type = env.get('CONTENT_TYPE')

        try:
            if content_type == 'application/json':
                return json.loads(data)

            return data
        except:
            raise BaseException('bad data')
