

class EngineModule:

    _engine = None

    alias = None

    def _on_init(
        self
    ):
        pass

    def __init__(
        self, engine
    ):
        self._engine = engine

        self._on_init()
