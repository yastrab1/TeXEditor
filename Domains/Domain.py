from datetime import datetime

from CubedCalendar.CalendarModel import CalendarModel


class Domain:

    def getCurrentSeries(self):
        for event in CalendarModel().getEvents():
            if datetime.today().date() > event.end:
                continue
            if datetime.today().date() < event.start:
                continue
            seriesNum = self.getSeriesNumberFromEventSummaryIfCorrect(event)
            if seriesNum != -1:
                return seriesNum

    def getSeriesNumberFromEventSummaryIfCorrect(self, event):
        """Method that takes event, returns -1 if the event is not the start of the series, otherwise returns the series number"""
        raise NotImplementedError("This is an abstract class, you have to derive it")

    def getName(self) -> str:
        raise NotImplementedError("This is an abstract class, you have to derive it")