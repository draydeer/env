

import json

from lib.driver import\
     Driver
from lib.errors import\
     NotExistsError


class FileJson(Driver):

    def g(
        self, k
    ):
        data = json.load(open(self._config['file']))

        if isinstance(data, dict) and k in data:
            return data[k]

        raise NotExistsError(k)
