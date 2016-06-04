

import json

from src.driver import Driver
from src.errors import NotExistsError


class FileJson(Driver):

    def g(self, k):
        data = json.load(open(self._config['file']))

        if isinstance(data, dict) and k in data:
            return data[k]

        raise NotExistsError("Key not exists: %s" % k)
