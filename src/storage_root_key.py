

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

    error = False
    k = None
    is_invalid = False
    last_sync = None
    prefix = None
    requested = 0
    type = None
    v = Value()

    def __init__(self, engine, k, driver, decryption_key=None, decryptor='aesBase64'):
        EngineModule.__init__(self, engine)

        self._decryption_key = decryption_key
        self._decryptor = decryptor
        self._driver = driver
        self.k = k

        self.update(True)

    def set_alias(self, value):
        self.alias = value

        return self

    def set_error(self, value):
        self.error = value

        return self

    def get_value(self):
        value = self.v.data

        return value

    def set_value(self, value=None, value_type=None):
        self.v = value if isinstance(value, Value) else Value(value, self.v.type if value_type is None else value_type)

        return self

    def get_type(self):
        value = self.v.type

        return value

    def event(self, event, *args, **kwargs):
        self._engine.event(event, self, *args, **kwargs)

        return self

    def g(self, k, default=None, decryption_key=None, decryptor=None):
        self.requested += 1

        r = self.v.data

        for x in k.split('.') if isinstance(k, str) else k:
            if isinstance(r, dict):
                r = r.get(x)

                continue

            if isinstance(r, list):
                r = r[int(x)] if x.isdigit() and len(r) > int(x) else None

                continue

            return default

        if isinstance(r, str) or isinstance(r, unicode):
            if decryption_key:
                return self._engine.cryptors_holder.get(decryptor or self._decryptor).decrypt(r, decryption_key)

        return r

    def invalidate(self):
        """
        Check if key has been changed and must be invalidated.

        :return: self
        """

        if json.dumps(self.v.data) != json.dumps(self._old):
            self._old = self.v.data

            self.event('key.invalidate')

        return self

    def update(self, throw=False):
        if self._driver:
            try:
                self.set_value(self._driver.g(self.k))
            except BaseException as e:
                self.error = True

                if throw:
                    raise e

        self.last_sync = time.time()

        return self
