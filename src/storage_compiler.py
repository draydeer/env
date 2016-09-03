

import os

from src.driver import Value
from src.engine_module import EngineModule
from src.errors import CircularReferenceError


class StorageCompiler(EngineModule):

    _key_compile_locks = {}
    _storage = None

    def __init__(self, engine, storage):
        EngineModule.__init__(self, engine)

        self._storage = storage

    def compile(self, key, val, allowed_rules={}, force_value=False):
        """
        Compile current key with checking for circular reference and parsing its value nested structure.

        :param key: Key.
        :param val: Value (document or simple value).
        :param allowed_rules: Set of allowed rules to be applied on rule values - [@@].
        :param force_value: Return initialized [Value] instead of raw data.
        :return:
        """
        if key in self._key_compile_locks:
            raise CircularReferenceError(key)

        self._key_compile_locks[key] = True

        # counter of encrypted values (has [@@:enc:<encrypted data>] format)
        encrypted_count = 0

        try:

            # another document as base pattern
            if isinstance(val, dict) and val.get('@@'):
                other = self._storage.g(val.get('@@'))

                if isinstance(other, dict):
                    other.update(val)

                    val = other

                    val.pop('@@')

            iterator = val.iteritems() if isinstance(val, dict) else enumerate(val) if isinstance(val, list) else None

            if iterator:
                patch = {}

                for iter_key, iter_val in iterator:

                    # rule value
                    if (isinstance(iter_val, str) or isinstance(iter_val, unicode)) is True and iter_val[0:2] == '@@':
                        path = iter_val.split(':')

                        if len(path) > 2:

                            # request another document and set as nested
                            if path[1] == 'env' and 'env' in allowed_rules:
                                patch[iter_key] = self._storage.g(path[2])

                                continue

                            # request os environment variable
                            if path[1] == 'var' and 'var' in allowed_rules:
                                patch[iter_key] = os.environ.get(path[2])

                                continue

                            # has encrypted data
                            if path[1] == 'enc':
                                encrypted_count += 1

                                continue

                    if isinstance(iter_val, dict) or isinstance(iter_val, list):
                        patch[iter_key] = self.compile(iter_key, iter_val, allowed_rules)

                if isinstance(val, dict):
                    val.update(patch)
                elif isinstance(val, list):
                    val = [patch[i] if i in patch else val for i, val in enumerate(val)]
        except BaseException as e:
            self._key_compile_locks.pop(key)

            raise e

        self._key_compile_locks.pop(key)

        return Value(val, encrypted_count=encrypted_count) if force_value else val
