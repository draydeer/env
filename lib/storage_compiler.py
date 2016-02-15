

import os

from lib.engine\
    import EngineModule
from lib.errors\
    import CyclicReferenceError
from lib.storage\
    import Storage
from packages.cast\
    import cast


class StorageCompiler(EngineModule):

    _key_compile_locks = {}
    _storage = None

    def __init__(
        self, engine, storage
    ):
        EngineModule.__init__(self, engine)

        self._storage = cast(storage, Storage)

    def compile(
        self, k, v
    ):
        if k in self._storage:
            raise CyclicReferenceError(k)

        self._key_compile_locks[k] = True

        if isinstance(v, dict) and v.get('@@'):
            other = self._storage.g(v.get('@@'))

            if isinstance(other, dict):
                other.update(v)

                v = other

                v.pop('@@')

        iter = v.iteritems() if isinstance(v, dict) else enumerate(v) if isinstance(v, list) else None

        if iter:
            replacement = {}

            for k, v in iter:
                if (isinstance(v, str) or isinstance(v, unicode)) and v[0:2] == '@@':
                    path = v.split(':')

                    if len(path) > 2:
                        if path[1] == 'env':
                            replacement[k] = self._storage.g(path[2])

                            continue

                        if path[1] == 'var':
                            replacement[k] = os.environ.get(path[2])

                            continue

                if isinstance(v, dict) or isinstance(v, list):
                    replacement[k] = self.compile(k, v)

            if isinstance(v, dict):
                v.update(replacement)
            elif isinstance(v, list):
                v = [replacement[i] if i in replacement else v for i, v in enumerate(v)]

        self._key_compile_locks.pop(k)

        return v
