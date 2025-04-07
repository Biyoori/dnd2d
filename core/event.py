class Event:
    _events = {}
    
    @classmethod
    def subscribe(cls, event_name, callback) -> None:
        if event_name not in cls._events:
            cls._events[event_name] = []
        cls._events[event_name].append(callback)

    @classmethod
    def unsubscribe(cls, event_name, callback) -> None:
        if event_name in cls._events:
            cls._events[event_name].remove(callback)

    @classmethod
    def notify(cls, event_name, *args, **kwargs) -> None:
        if event_name in cls._events:
            for callback in cls._events[event_name]:
                callback(*args, **kwargs)