
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


class Value(Dict, EngineModule):

    data = None
    encrypted_count = False
    type = None

    def __init__(self, engine, data=None, val_type=None, encrypted_count=0):
        EngineModule.__init__(self, engine)

        self.data = data
        self.encrypted_count = encrypted_count
        self.type = val_type

    def decrypt(self, decryption_key=None, data=None):
        if self.encrypted_count > 0:
            if data is None:
                data = self.data

    def g(self, path, default_value=None, decryption_key=None, decryptor=None):
        data = self.data

        for x in path.split('.') if isinstance(path, str) else path:
            if isinstance(data, dict):
                data = data.get(x)

                continue

            if isinstance(data, list):
                data = data[int(x)] if x.isdigit() and len(data) > int(x) else None

                continue

            return default_value

        return data
