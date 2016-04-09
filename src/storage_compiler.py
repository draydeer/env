import os

from src.engine_module import EngineModule
from src.errors import CircularReferenceError


class StorageCompiler(EngineModule):

    _key_compile_locks = {}
    _storage = None

    def __init__(
        self, engine, storage
    ):
        EngineModule.__init__(self, engine)

        self._storage = storage

    def compile(
        self, k, v
    ):
        if k in self._key_compile_locks:
            raise CircularReferenceError(k)

        self._key_compile_locks[k] = True

        try:
            if isinstance(v, dict) and v.get('@@'):
                other = self._storage.g(v.get('@@'))

                if isinstance(other, dict):
                    other.update(v)

                    v = other

                    v.pop('@@')

            iter = v.iteritems() if isinstance(v, dict) else enumerate(v) if isinstance(v, list) else None

            if iter:
                patch = {}

                for a, b in iter:
                    if (isinstance(b, str) or isinstance(b, unicode)) is True and b[0:2] == '@@':
                        path = b.split(':')

                        if len(path) > 2:
                            if path[1] == 'env':
                                patch[a] = self._storage.g(path[2])

                                continue

                            if path[1] == 'var':
                                patch[a] = os.environ.get(path[2])

                                continue

                    if isinstance(b, dict) or isinstance(b, list):
                        patch[a] = self.compile(a, b)

                if isinstance(v, dict):
                    v.update(patch)
                elif isinstance(v, list):
                    v = [patch[i] if i in patch else v for i, v in enumerate(v)]
        except BaseException as e:
            self._key_compile_locks.pop(k)

            raise e

        self._key_compile_locks.pop(k)

        return v