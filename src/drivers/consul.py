

import base64
import requests

from src.driver import Driver, Value
from src.errors import BadArgumentError, ConflictError, InternalError, NotExistsError


errors = {
    400: BadArgumentError,
    404: NotExistsError,
    409: ConflictError,
    500: InternalError,
}


class Consul(Driver):

    def g(
        self, k
    ):
        result = requests.request(
            'GET',
            'http://' + self._config.get('host', 'localhost:8500') + '/v1/kv/' + k,
            params={
                'recurse': self._config.recurse
            }
        )

        if result.status_code == 200:
            result = result.json()

            if self._config.recurse:
                d = {}

                for v in result:
                    keys = v['Key'][len(k) + 1:].split('/')

                    # if single key requested
                    if keys[0] == '':
                        return Value(base64.b64decode(result[0]['Value']))

                    temp = d

                    # reconstruct recursive keys
                    for i, key in enumerate(keys):
                        if i == len(keys) - 1:
                            break

                        if key not in temp or isinstance(temp[key], dict) is False:
                            temp[key] = {}

                        temp = temp[key]

                    temp[key] = base64.b64decode(v['Value'])

                return Value(d)

            return Value(base64.b64decode(result[0]['Value']))

        raise errors[result.status_code]() if result.status_code in errors else InternalError()
