import json
import re

from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat

import Runtime
from TextEditor.SyntaxHiglight.ColorMapInterpreter import ColorMapInterpreter
from TextEditor.TeXAnalyzer import TexAnalyzer


class SyntaxPattern:
    def __init__(self, regex: str, color: str, environment: str):
        self.regex = re.compile(regex, re.DOTALL)
        self.colorKey = color
        self.environment = environment

    @staticmethod
    def fromJson(json: dict, name: str):
        color = name
        environment = json[name]["environment"]
        regex = json[name]["regex"]
        return SyntaxPattern(regex, color, environment)
class Highlighter(QSyntaxHighlighter):
    def loadSyntaxPatternsFromCSV(self,path):
        with open(path,'r',encoding="utf-8") as config:
            text = json.loads(config.read())
            for key, value in text.items():
                self.patterns.append(SyntaxPattern.fromJson(text, key))

    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)
        self.highlight_format = QTextCharFormat()

        self.patterns = []
        self.loadSyntaxPatternsFromCSV("TextEditor\\SyntaxPatterns.json")

    def highlightBlock(self, text):
        analyzer = TexAnalyzer()
        analyzer.analyze(Runtime.Runtime().getData("EditorText"))

        for pattern in self.patterns:
            for match in pattern.regex.finditer(text):
                print(analyzer.getCurrentEnvironment(match.start())[-1].type)
                if not pattern.environment in analyzer.getCurrentEnvironment(match.start())[-1].type:
                    continue
                self.highlight_format = ColorMapInterpreter().interpret(pattern.colorKey, text)
                self.setFormat(match.start(), match.end() - match.start(), self.highlight_format)
