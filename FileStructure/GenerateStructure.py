import functools
import os
import webbrowser

from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QGroupBox, QCheckBox, QMessageBox

from Config.Config import Config
from CubedCalendar.CalendarModel import CalendarModel
from Dialogs.ConfigAskDialog import ConfigAskDialog
from Templates.TemplateCompiler import TemplateCompiler


class GenerateStructureButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Generate Structure")
        self.clicked.connect(self.onClick)
    def onClick(self):
        self.warningDialog = self.makeWarningToStart()
        result = self.warningDialog.exec()
        if result == QMessageBox.Cancel:
            return
        seminars = Config().get("CurrentSeminars")

        seminarExercises = {}
        for seminar in seminars:
            seminarExercises[seminar] = Config().get(f"Current{seminar}Exercises")

        rootDir = Config().get("RootDir")

        for seminar in seminars:
            path = os.path.join(rootDir,seminar)
            if not os.path.exists(path):
                os.mkdir(path)

            currentSeries = CalendarModel().getCurrentSeries(seminar)

            if not currentSeries:
                dialog = self.errorNoSeries(seminar)
                dialog.exec()
                continue

            seriesPath = os.path.join(path, f"{currentSeries}._seria")
            if not os.path.exists(seriesPath):
                os.mkdir(seriesPath)
            self.generateExerciseFile(seminar, seminarExercises, str(currentSeries), seriesPath)

    def generateExerciseFile(self, seminar, seminarExercises, currentSeries,seriesPath):
        for currentSeminarExercise in seminarExercises[seminar]:
            exercisePath = os.path.join(seriesPath, f"{currentSeminarExercise}_uloha.tex")
            with open(exercisePath, "w") as file:
                templatePath = Config().get(f"{seminar}ExerciseTemplate")
                templateText = ""
                with open(templatePath, "r") as file:
                    templateText = file.read()
                template = self.compileTemplate(templateText,seminar,currentSeries,currentSeminarExercise[:-1])
                with open(exercisePath,"w") as file:
                    file.write(template)

    def compileTemplate(self, templateText,seminar,series,excerciseNum):
        result = templateText
        for compiler in Config().get("TemplateCompilers"):
            result = TemplateCompiler(result, compiler,SEMINAR=seminar,SERIES=series,EXERCISE=excerciseNum).text
        return result

    def makeWarningToStart(self):
        dialog = QMessageBox()
        dialog.setWindowTitle("Are u sure?")
        dialog.setText(f"This will delete all files in the directory '{Config().get("RootDir")}'")
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        dialog.setIcon(QMessageBox.Warning)
        return dialog
    def errorNoSeries(self, seminarName):
        dialog = QMessageBox()
        dialog.setWindowTitle("Error")
        dialog.setText(f"There is no series currently going on in seminar {seminarName}")
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.setIcon(QMessageBox.Critical)
        return dialog




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
for seminarName in Config().get("SupportedSeminars"):
    Config().registerDialog(SelectSeminarExcercises,[f"Current{seminarName}Exercises"],[seminarName])
Config().registerDialog(SelectSeminars,["CurrentSeminars"])