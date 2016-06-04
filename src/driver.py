

from src.configurable import Configurable
from src.engine_module import EngineModule
from packages.serializer import Dict


class Driver(Configurable, EngineModule):

    _client = None

    def __init__(self, engine, config=None):
        Configurable.__init__(self, config)
        EngineModule.__init__(self, engine)

    def g(self, k):
        return None


class Value(Dict):

    data = None
    type = None

    def __init__(self, data=None, type=None):
        self.data = data
        self.type = type
