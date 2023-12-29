import string

from PyQt5.QtWidgets import QCompleter, QPlainTextEdit
from PyQt5.QtGui import QTextCursor, QFont
from PyQt5.QtCore import Qt

from AutoCompleter import AutoCompleter
from CubedCalendar.CalendarModel import CubedCalendar


class CustomTextEdit(QPlainTextEdit):
    keys = [Qt.Key_A,Qt.Key_B,Qt.Key_C,Qt.Key_D,Qt.Key_E,Qt.Key_F]
    def __init__(self, *args, **kwargs):
        super(CustomTextEdit, self).__init__(*args, **kwargs)

        self.completer = AutoCompleter()
        self.completer.setWidget(self)
        self.completer.insertText.connect(self.insertCompletion)
        font = QFont()
        font.setPixelSize(14)
        self.setFont(font)

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (len(completion) - len(self.completer.completionPrefix()))
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)
        self.completer.popup().hide()
    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        QPlainTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):

        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        if event.key() == (Qt.Key_Return or Qt.Key_Tab) and self.completer.popup().isVisible():
            current = len(tc.selectedText())

            self.insertText(self.completer.getSelected()[current:])
            self.completer.setCompletionMode(QCompleter.PopupCompletion)
            self.completer.popup().hide()
            return
        if event.text().endswith("\t"):
            self.insertText("    ")
            return
        self.processEvent(event)
        cr = self.cursorRect()

        if len(tc.selectedText()) > 0:
            print(tc.selectedText())
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


    def setText(self, text:str):
        self.setPlainText(text.replace("\t","    "))
        self.completer.onTextUpdated(self.toPlainText())
    def insertText(self,text:str):
        final = text

        self.insertPlainText(final)
    def processEvent(self,event):

        super().keyPressEvent(event)

