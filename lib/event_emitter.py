

class EventEmitter:

    _inst = None
    _key_index = 10000000
    _list = {}
    _list_flat = {}

    i = None

    def _ens(
        self, alias
    ):
        if self._list.get(alias) is None:
            self._list[alias] = {}

        return self._list[alias]

    def __call__(
        self, event, *args, **kwargs
    ):
        if event in self._list:
            for k, f in self._list[event].iteritems():
                f(*args, **kwargs)

        return self

    def event_detach(
        self, index
    ):
        self._list.get(
            self._list_flat.pop(index, 0), {}
        ).pop(index, 0)

        return self

    def event_subscribe(
        self, event, f
    ):
        self._ens(event)[self._key_index] = f
        self._list_flat[self._key_index] = event
        self._key_index += 1

        return self._key_index - 1

    def event_emit(
        self, event, *args, **kwargs
    ):
        if event in self._list:
            for k, f in self._list[event].iteritems():
                f(*args, **kwargs)

        return self


EventEmitter.i = EventEmitter()


class Ee:

    __ee = {}

    def event(
        self, event, *args, **kwargs
    ):
        EventEmitter.i.event_emit(event, *args, **kwargs)

    def event_detach(
        self, event
    ):
        on_event = 'on_' + event

        if hasattr(self, on_event) and event in self.__ee:
            EventEmitter.i.event_detach(self.__ee.pop(event))

        return self

    def event_subscribe(
        self, event
    ):
        on_event = 'on_' + event

        if hasattr(self, on_event) and event not in self.__ee:
            self.__ee[event] = EventEmitter.i.event_subscribe(event, getattr(self, on_event))

        return self
