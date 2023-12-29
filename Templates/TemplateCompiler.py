from Config.Config import Config


class TemplateCompiler:
    def __init__(self, text,compilerName,**knownProperties):
        self.text = text
        self.compilerName = compilerName
        self.replace(self.text,knownProperties)

    def replace(self, text,knownProperties:dict):
        print(knownProperties)
        properties = Config().get(f"{self.compilerName}Properties") + list(knownProperties.keys())
        result:str= text
        for prop in properties:
            value = None
            if prop in knownProperties.keys():
                value = knownProperties[prop]
            else:
                value = Config().get(prop)
            result = result.replace(prop, value)
        self.text = result
        return self.text