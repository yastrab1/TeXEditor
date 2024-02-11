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
        for currentProperty in properties:
            value = None
            if currentProperty in knownProperties.keys():
                value = knownProperties[currentProperty]
            else:
                value = Config().get(currentProperty)
            print(value)
            result = result.replace(currentProperty, value)
        self.text = result
        return self.text