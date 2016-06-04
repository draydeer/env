

import yaml

from src.driver import Driver
from src.errors import NotExistsError


class FileYaml(Driver):

    def g(self, k):
        data = yaml.load(open(self._config['file']))

        if isinstance(data, dict) and k in data:
            return data[k]

        raise NotExistsError("Key not exists: %s" % k)
