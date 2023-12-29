import re

from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout
from icalendar import Calendar

from CubedCalendar.EventLabel import Event

calendarPath = "CubedCalendar/any.ics"
from datetime import timedelta, date, datetime


class CalendarModel:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(CalendarModel, cls).__new__(cls)
        return cls.instance
    def load(self):
        self.events = []
        lines = ""
        with open(calendarPath, 'r',encoding="utf-8") as file:
            lines = file.read()

        calendar = Calendar.from_ical(lines)

        for component in calendar.walk():
            if component.name == "VEVENT":
                start = component.get("DTSTART").dt
                end = component.get("DTEND")
                if end:
                    end = end.dt

                summary = component.get("SUMMARY")
                description = component.get("DESCRIPTION")
                self.events.append(Event(start, end, summary, description))

        self.events.sort(key = lambda x:x.getStandardStart())
    def getCurrentSeries(self,seminarName):
        return 1
        # for event in self.events:
        #     if datetime.today().date() > event.end:
        #         continue
        #     if datetime.today().date() < event.start:
        #         continue
        #     pattern = re.compile(f"{seminarName} \\d+\\.séria")
        #     if pattern.match(event.summary):
        #         series = int(re.search("\\d+", event.summary))
        #         return series
class CubedCalendar(QFrame):
    def __init__(self):
        super().__init__()
        self.model = CalendarModel()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.model.load()
        self.generate()

    def generate(self):
        for event in self.model.events:
            start = event.start
            end = event.end
            title = f"{event.summary} -> {start} - {end}"
            label = QLabel(title)
            if date.today() <= start <= date.today() + timedelta(days=7) :
                label.setStyleSheet("QLabel { color : red; }")
            if start < date.today():
                label.setStyleSheet("QLabel { color : gray; }")
            self.layout.addWidget(label)