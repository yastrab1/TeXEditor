import calendar
from datetime import datetime, date, timedelta

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel


class EventLabel(QLabel):
    clicked = pyqtSignal(QLabel)

    def __init__(self, event, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.calendarEvent = event
        self.setText(f"{event.summary} | {event.start} - {event.end}")

        if date.today() <= event.start <= date.today() + timedelta(days=7):
            self.setStyleSheet("QLabel { color : red; }")
        if event.start < date.today():
            self.setStyleSheet("QLabel { color : gray; }")

    def mousePressEvent(self, event):
        self.clicked.emit(self)

    def getEvent(self):
        return self.calendarEvent

    def makeImportant(self):
        css = self.styleSheet()[8:-1]
        self.setStyleSheet("QLabel {" + css + " font-weight: bold;}")

    def makeUnimportant(self):
        css = self.styleSheet()[8:-1]
        self.setStyleSheet("QLabel {" + css + " font-weight: normal; }")
class Event:
    def __init__(self, start: datetime.date, end, summary, description, uid):
        self.summary = summary.encode("utf-8").decode("utf-8")
        self.start = start
        self.end = end
        self.uid = uid
        self.interested = False
        self.notifyBeforeHours = 0
        self.description = description.encode("utf-8").decode("utf-8")
        if end == None:
            self.end = self.start
    def getStandardStart(self):
        time = calendar.timegm(self.start.timetuple())
        return time
