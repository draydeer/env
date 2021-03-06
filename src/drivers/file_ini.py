
from ConfigParser import ConfigParser
from src.driver import Driver
from src.errors import NotExistsError


class FileIni(Driver):

    def g(self, k):
        data = ConfigParser()

        data.read(self._config['file'])

        data = {s: {k: v for (k, v) in data.items(s)} for s in data.sections()}

        if k in data:
            return data[k]

        raise NotExistsError("Key not exists: %s" % k)
