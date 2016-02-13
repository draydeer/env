

import requests

from lib.driver\
    import Driver, Value
from lib.errors\
    import NotExistsError


class FileYaml(Driver):

    def g(
        self, k
    ):
        result = requests.get(self._config['host'] + '/' + k + '/$')

        if result.status_code == 200:
            result = result.json()

            if 'v' in result:
                return Value(result['v'].get('v'), result['v'].get('type'))

        raise NotExistsError()
