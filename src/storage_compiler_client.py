import os

from src.engine_module import EngineModule
from src.errors import CircularReferenceError


class StorageCompiler(EngineModule):

    _key_compile_locks = {}
    _storage = None

    def __init__(self, engine, storage):
        EngineModule.__init__(self, engine)

        self._storage = storage

    def compile(self, k, v, allowed_rules={}):
        """
        Compile current key with checking for circular reference and parsing its value nested structure.

        :param k: Key.
        :param v: Value (document or simple value).
        :param allowed_rules: Set of allowed rules to be applied on rule values - [@@].
        :return:
        """
        if k in self._key_compile_locks:
            raise CircularReferenceError(k)

        self._key_compile_locks[k] = True

        try:

            # another document as base pattern
            if isinstance(v, dict) and v.get('@@'):
                other = self._storage.g(v.get('@@'))

                if isinstance(other, dict):
                    other.update(v)

                    v = other

                    v.pop('@@')

            iterator = v.iteritems() if isinstance(v, dict) else enumerate(v) if isinstance(v, list) else None

            if iterator:
                patch = {}

                for a, b in iterator:

                    # rule value
                    if (isinstance(b, str) or isinstance(b, unicode)) is True and b[0:2] == '@@':
                        path = b.split(':')

                        if len(path) > 2:

                            # request another document and set as nested
                            if path[1] == 'env' and 'env' in allowed_rules:
                                patch[a] = self._storage.g(path[2])

                                continue

                            # request os environment variable
                            if path[1] == 'var' and 'var' in allowed_rules:
                                patch[a] = os.environ.get(path[2])

                                continue

                    if isinstance(b, dict) or isinstance(b, list):
                        patch[a] = self.compile(a, b, allowed_rules)

                if isinstance(v, dict):
                    v.update(patch)
                elif isinstance(v, list):
                    v = [patch[i] if i in patch else v for i, v in enumerate(v)]
        except BaseException as e:
            self._key_compile_locks.pop(k)

            raise e

        self._key_compile_locks.pop(k)

        return v
