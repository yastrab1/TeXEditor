import functools
import webbrowser

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QCheckBox, QPushButton
from Config.Config import Config
from Dialogs.ConfigAskDialog import ConfigAskDialog


class SelectSeminars(ConfigAskDialog):
    def __init__(self):
        super().__init__()


        self.options = QGroupBox("Select Seminars that you compete in:")
        self.optionsLayout = QVBoxLayout()
        self.optionsWidgets = []

        for seminarName in Config().get("SupportedSeminars"):
            button = QCheckBox(seminarName)
            self.optionsLayout.addWidget(button)
            self.optionsWidgets.append(button)
        self.options.setLayout(self.optionsLayout)

        self.layout.addWidget(self.options)
        self.layout.addWidget(self.okButton)

    def collectData(self):
        result = {"CurrentSeminars":[]}
        for button in self.optionsWidgets:
            if button.isChecked():
                result["CurrentSeminars"].append(button.text())
        return result


class SelectSeminarExcercises(ConfigAskDialog):
    def __init__(self,seminarName):
        super().__init__()
        self.seminarName = seminarName

        self.options = QGroupBox(f"Select {seminarName} exercises you will compete in:")
        self.optionsLayout = QVBoxLayout()
        self.optionsList = []

        seminarExercises = Config().get(f"{seminarName}Exercises")
        for exercise in seminarExercises:
            button = QCheckBox(exercise)
            self.optionsLayout.addWidget(button)
            self.optionsList.append(button)

        self.openWebsiteButton = QPushButton("Open Website")
        self.openWebsiteButton.clicked.connect(functools.partial(webbrowser.open,Config().get(f"{self.seminarName}Website")))
        self.options.setLayout(self.optionsLayout)
        self.layout.addWidget(self.options)
        self.layout.addWidget(self.openWebsiteButton)
        self.layout.addWidget(self.okButton)


    def collectData(self) -> {}:
        result = {f"Current{self.seminarName}Exercises": []}
        for button in self.optionsList:
            if button.isChecked():
                result[f"Current{self.seminarName}Exercises"].append(button.text())
        return result
