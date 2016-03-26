

import requests

from lib.driver import\
     Driver, Value
from lib.errors import\
     BadArgumentError, ConflictError, InternalError, NotExistsError


errors = {
    400: BadArgumentError,
    404: NotExistsError,
    409: ConflictError,
    500: InternalError,
}


class Env(Driver):

    _client_id = None
    _remote = None

    def _on_init(
        self
    ):
        self._remote = self._config['host']

    def set_client_id(
        self, value
    ):
        self._client_id = value

        return self

    def set_remote(
        self, value
    ):
        self._remote = value

        return self

    def g(
        self, k
    ):
        result = requests.request(
            'INFO',
            self._remote + '/' + k
        )

        if result.status_code == 200:
            result = result.json()

            if 'v' in result:
                return Value(result['v'].get('v'), result['v'].get('type'))
            else:
                raise InternalError('corrupted data')

        raise errors[result.status_code](result.json()) if result.status_code in errors else InternalError()
