import json
import re

from PyQt5.QtWidgets import QTextEdit
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers.markup import TexLexer


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


class Highlighter:
    def __init__(self, parent: QTextEdit = None):
        self.parent = parent
        self.patterns = []
        self.loadSyntaxPatternsFromCSV("TextEditor\\SyntaxPatterns.json")
        self.lexer = TexLexer()
        self.formatter = HtmlFormatter(noclasses=True)
        self.parent.textChanged.connect(self.highlight)
        with open(r"C:\Users\Luki\PycharmProjects\TeXEditor\TextEditor\SyntaxHiglight\styles.css") as f:
            self.stylesheet = f.read()
        self.formatter.cssstyles = self.stylesheet

    def loadSyntaxPatternsFromCSV(self, path):
        with open(path, 'r', encoding="utf-8") as config:
            text = json.loads(config.read())
            for key, value in text.items():
                self.patterns.append(SyntaxPattern.fromJson(text, key))

    def highlight(self):
        oldCursorPos = self.parent.textCursor().position()
        formatted = highlight(self.parent.toPlainText(), self.lexer, self.formatter)
        print(formatted)
        self.parent.blockSignals(True)
        self.parent.setText(formatted)
        self.parent.setStyleSheet(self.stylesheet)
        tc = self.parent.textCursor()
        tc.setPosition(oldCursorPos)
        self.parent.setTextCursor(tc)
        self.parent.blockSignals(False)
