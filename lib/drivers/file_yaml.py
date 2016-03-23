

import yaml

from lib.driver import\
     Driver
from lib.errors import\
     NotExistsError


class FileYaml(Driver):

    def g(
        self, k
    ):
        data = yaml.load(open(self._config['file']))

        if isinstance(data, dict) and k in data:
            return data[k]

        raise NotExistsError(k)
