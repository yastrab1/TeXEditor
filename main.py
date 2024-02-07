import sys

from PyQt5.QtWidgets import QApplication

from MainWindow.MainWindow import MainWindow
from Runtime import Runtime, Hooks

if __name__ == "__main__":

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    Runtime().registerData("MainWindow", mainWindow)
    mainWindow.show()
    Runtime().emitHook(Hooks.APPSTART)
    state = app.exec_()
    Runtime().emitHook(Hooks.APPSTOP)
    sys.exit(state)

