

from lib.engine_module\
    import EngineModule


class TypeHandler(EngineModule):

    def __call__(
        self, **kwargs
    ):
        pass

    def get_config(
        self, k, d=None
    ):
        return self._engine.get_config().g('eventHandlers.keyInvalidate.' + self.alias + '.' + k, d)

    def has_config(
        self, k
    ):
        return self._engine.get_config().has('eventHandlers.keyInvalidate.' + self.alias + '.' + k)
