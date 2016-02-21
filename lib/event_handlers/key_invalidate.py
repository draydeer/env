

from lib.event_handler\
    import EventHandler
from lib.event_handlers.types.system_file\
    import SystemFile


class KeyInvalidate(EventHandler):

    _types = {}

    def _on_init(
        self
    ):
        self._types = {
            v.alias: v(self._engine) for v in filter(
                lambda x: self._engine.get_config().has('eventHandlers.keyInvalidate.' + x.alias),
                [
                    SystemFile,
                ]
            )
        }

    def __call__(
        self, value
    ):
        key_type = self._types.get(value.get_type())

        if key_type:
            key_type(**value.get_value())
