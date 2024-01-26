import os
import subprocess
import sys


from PyQt5.QtWidgets import *

from Config.Config import Config
from Runtime import Runtime, Hooks
from TextEditor.SideBar import SideBar
from TextEditor.SyntaxHighlight.SyntaxHighlighter import Highlighter
from TextEditor.TextEditor import CustomTextEdit


class LaTeXEditor(QWidget):
    def __init__(self):
        self.path = ""
        super().__init__()
        self.layout = QHBoxLayout()

        self.text_edit = CustomTextEdit()
        self.highlighter = Highlighter(self.text_edit)


        open_file_action = QAction('Open', self)
        open_file_action.setShortcut('Ctrl+O')
        open_file_action.triggered.connect(self.openFileDialog)

        save_file_action = QAction('Save', self)
        save_file_action.setShortcut('Ctrl+S')
        save_file_action.triggered.connect(self.saveFile)

        menu = QMenuBar()
        file_menu = menu.addMenu('File')
        file_menu.addAction(open_file_action)
        file_menu.addAction(save_file_action)

        self.sidebar = SideBar()



        self.layout.setMenuBar(menu)
        splitter = QSplitter()
        splitter.addWidget(self.text_edit)
        splitter.addWidget(self.sidebar)
        self.layout.addWidget(splitter)

        self.setLayout(self.layout)
        self.setWindowTitle("PyQt5 Text Editor")
        self.setGeometry(100, 100, 1200, 600)


    def openFileDialog(self):
        self.path, _ = QFileDialog.getOpenFileName(self, 'Open File', "", "TeX Files (*.tex);;All Files (*)")
        if self.path:
            self.openFile(self.path)

    def openFile(self,path):
        self.path = path
        try:
            with open(path, 'r', encoding="utf-8") as file:
                self.text_edit.setEditorText(file.read())
                rootAbs = os.path.abspath(Config().get("RootDir"))
                self.setWindowTitle(os.path.relpath(rootAbs,path))
        except Exception as e:
            print(f"Error opening the file: {e}")

    def saveFile(self):
        if not self.path:
            self.path, _ = QFileDialog.getSaveFileName(self, 'Save File')

        try:
            with open(self.path, 'w', encoding="utf-8") as file:
                file.write(self.text_edit.toPlainText())
        except Exception as e:
            print(f"Error saving the file: {e}")

        try:
            self.generatePdf()
        except Exception as e:
            print(f"Error generating PDF: {e}")


    def generatePdf(self):
        print(self.path)
        result = subprocess.run(['pdflatex', self.path], cwd=os.path.dirname(self.path))
        renderedPath = ""
        if result.returncode == 0:  # pdflatex ran successfully
            renderedPath = self.path.replace(".tex", ".pdf")
        else:
            # handle error here, e.g., print an error message or throw an exception
            print('Error in running pdflatex')
        print(renderedPath)
        self.sidebar.openPdf(renderedPath)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    main_window = LaTeXEditor()
    Runtime().registerData("MainWindow", main_window)
    main_window.show()
    Runtime().emitHook(Hooks.APPSTART)
    state = app.exec_()
    Runtime().emitHook(Hooks.APPSTOP)
    sys.exit(state)

