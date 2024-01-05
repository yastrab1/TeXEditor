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
        regex = r"\\.*?[{\s\n(]"
        matches = re.findall(regex, text,re.DOTALL)
        for match in matches:
            if match not in self.keywords:
                self.keywords.append(match.lstrip("\\"))
        self.keywords = list(set(self.keywords))
        self.model().setStringList([*self.keywords])
        self.saveKeywords()

    def setHighlighted(self, text):
        self.lastSelected = text

    def getSelected(self):
        return self.lastSelected

    def closeEvent(self, a0):
        self.saveKeywords()
