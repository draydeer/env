
from src.engine_module import EngineModule
from packages.config import Config


class TypeHandler(EngineModule):

    def __call__(self, **kwargs):
        pass

    def get_config(self, k):
        return Config(self._engine.get_config().g('eventHandlers.keyInvalidate.' + self.alias + '.' + k))

    def has_config(self, k):
        return self._engine.get_config().has('eventHandlers.keyInvalidate.' + self.alias + '.' + k)
