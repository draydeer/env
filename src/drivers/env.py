
import requests

from src.driver import Driver, Value
from src.errors import BadArgumentError, ConflictError, InternalError, NotExistsError


errors = {
    400: BadArgumentError,
    404: NotExistsError,
    409: ConflictError,
    500: InternalError,
}


class Env(Driver):

    _remote = None

    def _on_init(self):
        self._remote = self._config['host']

        self.event_subscribe('society_populate')

    def set_remote(self, value):
        self._remote = value

        return self

    def g(self, k):
        result = requests.request(
            'INFO',
            self._remote + '/' + k,
            params={
                'clientId': self._engine.client_id
            }
        )

        if result.status_code == 200:
            result = result.json()

            if 'v' in result:
                return Value(result['v'].get('v'), result['v'].get('type'))
            else:
                raise InternalError('Corrupted data.')

        raise errors[result.status_code](result.json()) if result.status_code in errors else InternalError()

    def on_society_populate(self):

        # if remote left select new one
        if self._engine.society.has(self._remote) is False:
            self._remote = self._engine.society.select()
