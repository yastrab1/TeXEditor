import calendar
from datetime import datetime

from PyQt5.QtWidgets import QLabel


class EventLabel(QLabel):
    def __init__(self,event):
        super().__init__()
        self.event = event
    def mouseDoubleClickEvent(self, a0):
        pass

class Event:
    def __init__(self,start:datetime.date,end,summary,description):
        self.summary = summary.encode("utf-8").decode("utf-8")
        self.start = start
        self.end = end
        self.description = description.encode("utf-8").decode("utf-8")
        if end == None:
            self.end = self.start
    def getStandardStart(self):
        time = calendar.timegm(self.start.timetuple())
        return time
