import os

from PyQt5.QtWidgets import QPushButton, QMessageBox

from Config.Config import Config
from CubedCalendar.CalendarModel import CalendarModel
from Dialogs.SeminarAskingDialogs import SelectSeminars, SelectSeminarExcercises
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
        seminars:list[str] = Config().get("CurrentSeminars")

        seminarExercises = {}
        for seminar in seminars:
            seminarExercises[seminar] = Config().get(f"Current{seminar}Exercises")

        rootDir = Config().get("RootDir")

        for seminar in seminars:
            path = os.path.join(rootDir,seminar)
            if not os.path.exists(path):
                os.mkdir(path)

            currentSeries = CalendarModel().getCurrentSeriesOfSeminar(seminar)

            if not currentSeries:
                dialog = self.errorNoSeries(seminar)
                dialog.exec()
                continue

            seriesPath = os.path.join(path, f"{currentSeries}._seria")
            if not os.path.exists(seriesPath):
                os.mkdir(seriesPath)
            self.generateExerciseFiles(seminar, seminarExercises, str(currentSeries),seriesPath)

    def generateExerciseFiles(self, seminar, seminarExercises, currentSeries,seriesPath):
        for currentSeminarExercise in seminarExercises[seminar]:
            self.generateExerciseFile(seminar, currentSeminarExercise, currentSeries, seriesPath)

    def generateExerciseFile(self, seminar, currentSeminarExercise, currentSeries, seriesPath):
        exercisePath = os.path.join(seriesPath, f"{currentSeminarExercise}_uloha.tex")
        templatePath = Config().get(f"{seminar}ExerciseTemplate")

        rawTemplate = ""
        with open(templatePath, "r", encoding="utf-8") as file:
            rawTemplate = file.read()
        finalTemplate = self.compileTemplate(rawTemplate, seminar, currentSeries, currentSeminarExercise[:-1])
        with open(exercisePath, "w", encoding="utf-8") as file:
            file.write(finalTemplate)

    def compileTemplate(self, templateText,seminar,series,excerciseNum):
        result = templateText
        for compiler in Config().get("TemplateCompilers"):
            result = TemplateCompiler(result, compiler,SEMINAR=seminar,SERIES=series,EXERCISE=excerciseNum).text
        return result

    def makeWarningToStart(self):
        dialog = QMessageBox()
        dialog.setWindowTitle("Are u sure?")
        dialog.setText("This will delete all files in the directory "+Config().get("RootDir"))
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        dialog.setIcon(QMessageBox.Warning)
        return dialog
    def errorNoSeries(self, seminarName):
        dialog = QMessageBox()
        dialog.setWindowTitle("Error")
        dialog.setText("There is no series currently going on in seminar "+seminarName)
        dialog.setStandardButtons(QMessageBox.Ok)
        dialog.setIcon(QMessageBox.Critical)
        return dialog


