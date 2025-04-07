class Event:
    def __init__(self) -> None:
        self.subscribers = []
    
    def subscribe(self, callback):
        self.subscribers.append(callback)

    def notify(self, *args, **kwargs):
        for callback in self.subscribers:
            callback(*args, **kwargs)