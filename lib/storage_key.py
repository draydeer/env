

import json
import time


from lib.driver\
    import Value
from packages.serializer\
    import Dict


class StorageKey(Dict):

    _decryption_key = None
    _driver = None
    _engine = None
    _old = None

    k = None
    is_invalid = False
    last_sync = None
    requested = 0
    type = None
    v = Value()

    def __init__(
        self, engine, k, driver, decryption_key=None
    ):
        self._decryption_key = decryption_key
        self._driver = driver
        self._engine = engine
        self.k = k

        self.update(True)

    def get_value(
        self
    ):
        value = self.v.data

        return value

    def set_value(
        self, value=None, type=None
    ):
        self.v = value if isinstance(value, Value) else Value(value, self.v.type if type is None else type)

        return self

    def get_type(
        self
    ):
        value = self.v.type

        return value

    def g(
        self, k, d=None
    ):
        self.requested += 1

        r = self.v.data

        for x in k.split('.') if isinstance(k, str) else k:
            if isinstance(r, dict):
                r = r.get(x)

                continue

            if isinstance(r, list):
                r = r[int(x)] if x.isdigit() and len(r) > int(x) else None

                continue

            return d

        return r

    def invalidate(
        self
    ):
        if json.dumps(self.v.data) != json.dumps(self._old):
            self._old = self.v.data

            self.send_event('key.invalidate')

        return self

    def send_event(
        self, event
    ):
        self._engine.event(event, self)

        return self

    def update(
        self, throw=False
    ):
        if self._driver:
            try:
                self.set_value(self._driver.g(self.k))
            except BaseException as e:
                if throw:
                    raise e

        self.last_sync = time.time()

        return self
