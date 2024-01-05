import re

from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat

from TextEditor.SyntaxHiglight.ColorMapInterpreter import ColorMapInterpreter


class SyntaxPattern:
    def __init__(self,regex:str,color):
        self.regex = re.compile(regex, re.DOTALL)
        self.color = color
class Highlighter(QSyntaxHighlighter):
    def loadSyntaxPatternsFromCSV(self,path):
        with open(path,'r',encoding="utf-8") as config:
            for line in config.read().split("\n"):
                if line == "":
                    continue
                lineArgs = line.split(";")
                pattern = SyntaxPattern(lineArgs[0],lineArgs[1])
                self.patterns.append(pattern)

    def __init__(self, parent=None):
        super(Highlighter, self).__init__(parent)
        self.highlight_format = QTextCharFormat()

        self.patterns = []
        self.loadSyntaxPatternsFromCSV("TextEditor\\SyntaxPatterns.txt")

    def highlightBlock(self, text):
        for pattern in self.patterns:
            for match in pattern.regex.finditer(text):
                self.highlight_format = ColorMapInterpreter().interpret(pattern.color)
                self.setFormat(match.start(), match.end() - match.start(), self.highlight_format)
