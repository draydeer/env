
from src.event_emitter import Ee


class EngineModule(Ee):

    _engine = None

    alias = None

    def _on_init(self):
        pass

    def __init__(self, engine):
        self._engine = engine

        self._on_init()

    @property
    def alive(self):
        return self._engine.alive

    @property
    def logger(self):
        return self._engine.logger
