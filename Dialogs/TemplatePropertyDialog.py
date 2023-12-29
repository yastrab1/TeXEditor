from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QLineEdit

from Config.Config import Config
from Dialogs.ConfigAskDialog import ConfigAskDialog


class TemplatePropertyDialog(ConfigAskDialog):
    def __init__(self,propertyName):
        super().__init__(self)
        self.propertyName = propertyName
        self.setWindowTitle("Property ask")
        self.introLabel = QLabel("While generating a template, there is a property that has not been set:")

        self.subwidget = QWidget(self)
        self.sublayout = QHBoxLayout(self.subwidget)

        self.label = QLabel(propertyName+":")

        self.lineInput = QLineEdit()

        self.sublayout.addWidget(self.label)
        self.sublayout.addWidget(self.lineInput)
        self.subwidget.setLayout(self.sublayout)

        self.layout.addWidget(self.introLabel)
        self.layout.addWidget(self.subwidget)
        self.layout.addWidget(self.okButton)
    def collectData(self) -> {}:
        return {self.propertyName:self.lineInput.text()}