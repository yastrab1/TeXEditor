from typing import Callable
class OnCloseObserver:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(OnCloseObserver, cls).__new__(cls)
        return cls.instance

    def register(self, receiver:Callable):
        if not hasattr(self,"receivers"):
            self.receivers = []
        self.receivers.append(receiver)
    def trigger(self):
        for receiver in self.receivers:
            receiver()