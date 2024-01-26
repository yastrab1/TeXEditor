from PyQt5.QtWidgets import QTextEdit
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers.markup import TexLexer

from Config.Config import Config


class Highlighter:
    def __init__(self, parent: QTextEdit = None):
        self.parent = parent
        self.patterns = []

        self.lexer = TexLexer()
        self.formatter = HtmlFormatter(noclasses=True, cssfile=Config().get("SyntaxStyles"))
        self.parent.textChanged.connect(self.highlight)

    def highlight(self):
        oldCursorPos = self.parent.textCursor().position()
        formatted = highlight(self.parent.toPlainText(), self.lexer, self.formatter)
        print(formatted)
        self.parent.blockSignals(True)

        self.parent.setText(formatted)
        tc = self.parent.textCursor()
        tc.setPosition(oldCursorPos)
        self.parent.setTextCursor(tc)

        self.parent.blockSignals(False)
