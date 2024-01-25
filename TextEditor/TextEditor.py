import pyautogui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QTextEdit

import Runtime
from Defaults import FontDefaults
from TextEditor.AutoCompleter import AutoCompleter


class CustomTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super(CustomTextEdit, self).__init__(*args, **kwargs)

        self.completer = AutoCompleter()
        self.completer.setWidget(self)

        self.setFont(FontDefaults.classicFont)

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        super().focusInEvent(event)

    def keyPressEvent(self, event):

        Runtime.Runtime().registerData("EditorText", self.toPlainText())
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        key = event.key()
        if (key == Qt.Key_Return or key == Qt.Key_Tab) and self.completer.popup().isVisible():

            current = len(tc.selectedText())
            toInsert = self.completer.getSelected()[current:]
            total = tc.selectedText() + toInsert
            print(total)
            tc.beginEditBlock()
            self.insertText(toInsert)
            if "{" in toInsert:
                index = toInsert.index("{")
                for i in range(len(toInsert) - index - 1):
                    pyautogui.keyDown("left")
            if "begin" in total:
                self.insertText("\n\\end{}")
            self.completer.popup().hide()
            tc.endEditBlock()
            return
        if event.text().endswith("\t"):
            self.insertText("    ")
            return
        self.processEvent(event)
        cr = self.cursorRect()

        if len(tc.selectedText()) > 0:
            self.completer.setCompletionPrefix(tc.selectedText())
            popup = self.completer.popup()
            popup.setCurrentIndex(self.completer.completionModel().index(0, 0))

            cr.setWidth(self.completer.popup().sizeHintForColumn(0)
                        + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cr)

        else:
            self.completer.popup().hide()
        if event.text().endswith("{"):
            self.insertText("}")

        tc.select(QTextCursor.WordUnderCursor)

    def setEditorText(self, text: str):
        self.setText(text.replace("\t", "    "))
        self.completer.onTextUpdated(self.toPlainText())

    def insertText(self, text: str):
        final = text

        self.insertPlainText(final)

    def processEvent(self, event):
        super().keyPressEvent(event)
