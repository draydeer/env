

import requests

from lib.driver\
    import Driver, Value
from lib.errors\
    import BadArgumentError, ConflictError, InternalError, NotExistsError


errors = {
    400: BadArgumentError,
    404: NotExistsError,
    409: ConflictError,
    500: InternalError,
}


class Env(Driver):

    def g(
        self, k
    ):
        result = requests.get(self._config['host'] + '/' + k + '/$')

        if result.status_code == 200:
            result = result.json()

            if 'v' in result:
                return Value(result['v'].get('v'), result['v'].get('type'))
            else:
                raise InternalError('corrupted data')

        raise errors[result.status_code](result.json()) if result.status_code in errors else InternalError()
