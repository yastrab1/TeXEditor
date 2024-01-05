import re

from PyQt5 import QtCore
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QCompleter

keywordPath = "keywords.txt"
class AutoCompleter(QCompleter):
    insertText = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()
        QCompleter.__init__(self, [], parent)
        self.keywords = []
        self.loadKeywords()
        super().setModel(QStringListModel(self.keywords))

        self.setCompletionMode(QCompleter.PopupCompletion)
        self.highlighted.connect(self.setHighlighted)

    def loadKeywords(self):
        with open(keywordPath,'r',encoding="utf-8") as file:
            self.keywords = file.read().split()

    def saveKeywords(self):
        with open(keywordPath,'w',encoding="utf-8") as file:
            file.write("\n".join(self.keywords))

    def onTextUpdated(self,text):
        commands = self.findLatexCommandsAndSignatures(text)
        self.keywords = list(set(commands))
        self.model().setStringList([*self.keywords])
        self.saveKeywords()

    def findLatexCommandsAndSignatures(self, content):
        def wrapSignatureInOriginalParenthesis(signature, original):
            if not original:
                return
            return original[0] + signature + original[-1]

        # Regular expression to match LaTeX commands with their arguments
        regex_pattern = r'\\([a-zA-Z]+)(\*?)(\[[^\]]*\])?(\{[^\}]*\})?'

        matches = re.finditer(regex_pattern, content)

        latex_commands = []
        for match in matches:
            command_name = match.group(1)
            star_modifier = wrapSignatureInOriginalParenthesis("", match.group(2))
            optional_argument = wrapSignatureInOriginalParenthesis("", match.group(3))
            mandatory_argument = wrapSignatureInOriginalParenthesis("", match.group(4))

            # Construct the signature of the LaTeX command
            signature = f"{command_name}"
            if star_modifier:
                signature += "*"
            if optional_argument:
                signature += optional_argument
            if mandatory_argument:
                signature += mandatory_argument

            latex_commands.append(signature)

        return latex_commands

    def setHighlighted(self, text):
        self.lastSelected = text

    def getSelected(self):
        return self.lastSelected

    def closeEvent(self, a0):
        self.saveKeywords()
