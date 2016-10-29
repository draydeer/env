
import json
import time

from src.driver import Value
from src.engine_module import EngineModule
from packages.serializer import Dict


class StorageRootKey(EngineModule, Dict):

    _decryption_key = None
    _decryptor = None
    _driver = None
    _engine = None
    _old = None
    _value = None

    error = False
    key = None
    is_invalid = False
    last_sync = None
    prefix = None
    requested = 0
    # type = None

    def __init__(self, engine, k, driver, decryption_key=None, decryptor='aesBase64'):
        EngineModule.__init__(self, engine)

        self._decryption_key = decryption_key
        self._decryptor = decryptor
        self._driver = driver
        self._value = Value(engine)
        self.key = k

        self.update(True)

    @property
    def value(self):
        return self._value.data

    @value.setter
    def value(self, value):
        self.set_value(value)

    @property
    def type(self):
        return self._value.type

    def set_alias(self, value):
        self.alias = value

        return self

    def set_error(self, value):
        self.error = value

        return self

    def set_value(self, mixed=None, val_type=None):
        if isinstance(mixed, Value):
            self._value = mixed
        else:
            self._value = Value(self._engine, mixed, self._value.type if val_type is None else val_type)

        return self

    def event(self, event, *args, **kwargs):
        self._engine.event(event, self, *args, **kwargs)

        return self

    def g(self, path, default_value=None, decryption_key=None, decryptor=None):
        self.requested += 1

        data = self._value.data

        for x in path.split('.') if isinstance(path, str) else path:
            if isinstance(data, dict):
                data = data.get(x)

                continue

            if isinstance(data, list):
                data = data[int(x)] if x.isdigit() and len(data) > int(x) else None

                continue

            return default_value

        if decryption_key:
            if isinstance(data, str) or isinstance(data, unicode):
                return self._engine.cryptors_holder.get(decryptor or self._decryptor).decrypt(data, decryption_key)
            elif self._value.data_encrypted_count:
                """
                Decrypt complex structure.
                """
                if isinstance(data, dict) or isinstance(data, list):
                    pass

        return data

    def invalidate(self):
        """
        Check if key has been changed and must be invalidated.

        :return: self
        """
        if json.dumps(self._value.data) != json.dumps(self._old):
            self._old = self._value.data

            self.event('key.invalidate')

        return self

    def update(self, throw=False):
        if self._driver:
            try:
                self.set_value(self._driver.g(self.key))
            except BaseException as e:
                self.error = True

                if throw:
                    raise e

        self.last_sync = time.time()

        return self
