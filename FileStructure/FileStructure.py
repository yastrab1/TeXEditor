import os.path
import shutil

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtWidgets import QTreeView, QWidget, QVBoxLayout, QMessageBox, QLabel

from Config.Config import Config
from FileStructure.GenerateStructure import GenerateStructureButton
from Runtime import Runtime

ROOT_DIR = Config().get("RootDir")


class FileStructureLeafItem(QLabel):
    def __init__(self, path):
        super().__init__()
        self.setText(os.path.basename(path))
class FileStructureTreeView(QTreeView):
    def __init__(self):

        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete and self.currentIndex().isValid():
            path = self.currentIndex().model().filePath(self.currentIndex())
            if self.showWarningDialogOnDelete(path) == QMessageBox.Ok:
                shutil.rmtree(path)

    def showWarningDialogOnDelete(self, path):
        box = QMessageBox()
        box.setIcon(QMessageBox.Warning)
        box.setText(f"Are you sure you want to delete {os.path.basename(path)}?")
        box.setWindowTitle("Are u sure?")
        return box.exec()


class FileStructure(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        if not os.path.exists(ROOT_DIR):
            os.mkdir(ROOT_DIR)

        self.fileModel = QFileSystemModel()
        self.fileModel.setRootPath(ROOT_DIR)
        self.setLayout(self.layout)
        self.fileView = FileStructureTreeView()
        self.fileView.setModel(self.fileModel)

        self.fileView.doubleClicked.connect(self.onDoubleClicked)

        self.generateStructureButton = GenerateStructureButton()

        self.setLayout(self.layout)
        self.layout.addWidget(self.generateStructureButton)
        self.layout.addWidget(self.fileView)

        self.fileView.setRootIndex(self.fileModel.index(ROOT_DIR))

    def onDoubleClicked(sel, arg):
        filepath = arg.model().filePath(arg)
        if os.path.isdir(filepath):
            return
        window = Runtime().getData("MainWindow")
        window.openFile(arg.model().filePath(arg))
