
import json
from typing import re

from fernet import Fernet

from OnCloseObserver import OnCloseObserver

CONFIG_FILE = "config.json"
class Config:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)

            cls.instance.init()
        return cls.instance

    def init(self):

        self.config = {}
        self.configAskingDialogs = {}

        self.saveConfigCallbacks = []
        self.loadConfigCallbacks = []

        PasswordManager().init()  # TODO somracky sposob riesenia tohto problemu, toto je temporary

        self.loadConfig()

        OnCloseObserver().register(self.saveConfig)

    def loadConfig(self):
        with open(CONFIG_FILE,"r",encoding="utf-8") as file:
            text = file.read()
            raw = json.loads(text)
        self.config = self.applyCallbacksOnConfig(raw, self.loadConfigCallbacks)

    def applyCallbacksOnConfig(self, config, callbacks):
        if len(callbacks) == 0:
            return config

        result = {}
        for key in config.keys():
            if key.endswith("Password"):
                pass
            options = [callback(key, config[key]) for callback in callbacks]

            if len(options) > 2:
                raise Exception(f"Multiple callbacks deserialized key {key} differently")
            if len(options) == 1:
                result[key] = options[0]
                continue
            options.remove(config[key])
            result[key] = options[0]
        return result

    def saveConfig(self):
        serialized = self.applyCallbacksOnConfig(self.config, self.saveConfigCallbacks)
        with open(CONFIG_FILE,"w",encoding="utf-8") as file:
            file.write(json.dumps(serialized, indent=4))

    def get(self,key):
        if key in self.config:
            return self.config[key]
        if f"{key}Default" in self.config:
            return self.config[f"{key}Default"]

        if not key in self.configAskingDialogs.keys():
            raise ValueError(f"No config with key {key}")

        args = self.configAskingDialogs[key][1]
        if not args:
            dialog = self.configAskingDialogs[key][0]()
        else:
            dialog = self.configAskingDialogs[key][0](*self.configAskingDialogs[key][1])
        newConfig = dialog.askConfig()


        for name,value in newConfig.items():
            self.config[name] = value
        return self.config[key]

    def findRegex(self, regex):
        keys = self.config.keys()
        result = []
        for key in keys:
            if re.match(regex, key):
                result.append(key)
        return result
    def registerDialog(self,dialog,configThatItAsks,args = None):
        for config in configThatItAsks:
            self.configAskingDialogs[config] = dialog,args

    def addSaveConfigCallback(self, callback):
        self.saveConfigCallbacks.append(callback)

    def addLoadConfigCallback(self, callback):
        self.loadConfigCallbacks.append(callback)


class PasswordManager:
    def init(self):
        with open("secret.txt", "r", encoding="utf-8") as f:
            self.key = bytes(f.read(), "utf-8")
        if self.key == b"":
            self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

        Config().addLoadConfigCallback(self.deserialize)
        Config().addSaveConfigCallback(self.serialize)

        OnCloseObserver().register(self.saveKey)

    def saveKey(self):
        with open("secret.txt", "w", encoding="utf-8") as f:
            f.write(self.key.decode("utf-8"))

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(PasswordManager, cls).__new__(cls)
        return cls.instance

    def serialize(self, key, value):
        if not isinstance(key, str):
            return value
        if not key.endswith("Password"):
            return value
        return self.fernet.encrypt(value).decode("utf-8")

    def deserialize(self, key, value):
        if not isinstance(value, str):
            return value
        if not key.endswith("Password"):
            return value
        return self.fernet.decrypt(bytes(value, "utf-8")).decode("utf-8")
