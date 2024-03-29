from enum import Enum
class Runtime:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance
    def registerData(self,key,value):
        if not hasattr(self,"data"):
            self.data = {}
        self.data[key] = value
    def getData(self,key):
        if key not in self.data:
            return None
        return self.data[key]

    def registerHook(self, name, callback):
        if not hasattr(self, "callbacks"):
            self.callbacks = {}
        if not name in self.callbacks.keys():
            self.callbacks[name] = []
        self.callbacks[name].append(callback)

    def emitHook(self, name):
        for callback in self.callbacks[name]:
            callback()


class Hooks(Enum):
    APPSTART = 1
    APPSTOP = 2
    TEXANALYZEFINISH = 3
