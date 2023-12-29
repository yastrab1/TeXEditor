
import json
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
        self.loadConfig()

        OnCloseObserver().register(self.saveConfig)

    def loadConfig(self):
        with open(CONFIG_FILE,"r",encoding="utf-8") as file:
            text = file.read()

            self.config = json.loads(text)
    def saveConfig(self):
        with open(CONFIG_FILE,"w",encoding="utf-8") as file:
            file.write(json.dumps(self.config,indent=4))
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
    def registerDialog(self,dialog,configThatItAsks,args = None):
        for config in configThatItAsks:
            self.configAskingDialogs[config] = dialog,args
