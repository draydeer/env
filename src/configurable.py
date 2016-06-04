

from packages.config import Config


class Configurable(object):

    _config = None

    def _on_init(self):
        pass

    def __init__(self, config):
        self.config = config

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = Config(config)

        self._on_init()
