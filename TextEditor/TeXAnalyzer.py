import re


class Environment:
    def __init__(self, start, end, type):
        self.start = start
        self.end = end
        self.type = type


class TexAnalyzer:
    def __init__(self):
        self.environments = []

    def analyze(self, text):
        self.environments = []
        beginRegex = re.compile(r"\\begin\{([^}]+)\}(.*?)(\\end\{\1\})", re.DOTALL)
        environmentsText = re.finditer(beginRegex, text)
        for environment in environmentsText:
            self.environments.append(Environment(environment.start(), environment.end(), environment.group(1)))

    def getCurrentEnvironment(self, index):
        environments = [Environment(0, 10000000000000, "")]
        for environment in self.environments:
            if environment.start <= index <= environment.end:
                environments.append(environment)
        return environments
