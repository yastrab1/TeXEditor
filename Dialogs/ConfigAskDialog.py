from typing import Callable

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QInputDialog, QPushButton, QDialog
from Config.Config import Config
class ConfigAskDialog(QDialog):
    def __init__(self,propertiesThatItAsks):
        super().__init__()
        self.layout = QVBoxLayout()

        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(self.close)


        self.setLayout(self.layout)


    def askConfig(self) -> {}:
        self.exec()
        return self.collectData()

    def collectData(self) -> {}:
        pass