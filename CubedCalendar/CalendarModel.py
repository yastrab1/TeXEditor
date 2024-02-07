import json
import os.path
from datetime import datetime, timedelta

import numpy
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox
from icalendar import Calendar

from Config.Config import Config
from CubedCalendar.EventLabel import Event
from Domains.DomainFactorySingleton import DomainFactorySingleton
from Runtime import Runtime, Hooks

calendarPath = "CubedCalendar/any.ics"
interestedEventsPath = "CubedCalendar/interestedEvents.json"
import requests


class CalendarModel:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "instance"):
            cls.instance = super(CalendarModel, cls).__new__(cls)
            cls.instance.init()
        return cls.instance

    def init(self):
        self.events = []
        self.interestedEvents = {}

        Runtime().registerHook(Hooks.APPSTOP, self.saveInterestedEvents)

    def saveInterestedEvents(self):
        data = {}
        for event in self.events:
            if not event.interested:
                continue
            data[event.uid] = {"hours": event.notifyBeforeHours}
        with open(interestedEventsPath, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=4))

    def loadInterestedEvents(self):
        if not os.path.exists(interestedEventsPath):
            with open(interestedEventsPath, "w", encoding="utf-8") as file:
                pass
        with open(interestedEventsPath, "r", encoding="utf-8") as file:
            text = file.read()
            if text == "":
                return
            data = json.loads(text)
        for uid, eventdata in data.items():
            event = self.getEventFromUID(uid)
            event.interested = True
            event.notifyBeforeHours = eventdata["hours"]
        for seminar in Config().get("CurrentSeminars"):
            for event in self.events:
                if seminar in event.summary:
                    event.interested = True

    def importFromInternet(self):
        data = ""
        try:
            data = self._importFromInternetUnhandled()
        except requests.ConnectionError as e:
            self.makeErrorBox()
        if not data:
            with open(interestedEventsPath, 'r', encoding="utf-8") as file:
                data = file.read()
        return data

    def _importFromInternetUnhandled(self):
        response = requests.request("GET", "https://ical.kockatykalendar.sk/any/any.ics")
        response.encoding = "utf-8"
        data = response.text
        self.cacheData(data)
        return data

    def cacheData(self, data):
        with open(calendarPath, 'w', encoding="utf-8") as file:
            file.write(data)
    def load(self):
        data = self.importFromInternet()
        self.events = []
        calendar = Calendar.from_ical(data)
        for component in calendar.walk():
            if component.name == "VEVENT":
                start = component.get("DTSTART").dt
                end = component.get("DTEND")
                if end:
                    end = end.dt

                summary = component.get("SUMMARY")
                description = component.get("DESCRIPTION")
                uid = component.get("UID")
                self.events.append(Event(start, end, summary, description, uid))

        self.events.sort(key=lambda x: x.getStandardStart())
        self.loadInterestedEvents()
        self.spawnNotificationTimers()

    def spawnNotificationTimers(self):
        for event in self.events:
            if not event.interested:
                continue
            eventdatetime = datetime.combine(event.start, datetime.min.time())
            differenceStartToday = (eventdatetime - datetime.today())
            diff = differenceStartToday - timedelta(hours=event.notifyBeforeHours)
            diff = numpy.clip(diff.total_seconds() * 1000, 0, 2147483647)
            if differenceStartToday.total_seconds() < 0:
                continue

            timer = QTimer.singleShot(int(diff), self.makeNotificationWrapper(event))

    def makeNotificationWrapper(self, event):
        def makeNotification():
            eventdatetime = datetime.combine(event.start, datetime.min.time())
            box = QMessageBox()
            box.setIcon(QMessageBox.Information)
            box.setWindowTitle(event.summary)
            box.setText(f"{event.summary}\n Starts in: {(eventdatetime - datetime.today())}")
            box.exec()

        return makeNotification

    def makeErrorBox(self):
        box = QMessageBox()
        box.setIcon(QMessageBox.Critical)
        box.setWindowTitle("Error while loading Calendar options")
        box.setText(
            "Failed loading Calendar from internet. Check your internet connection\nUsing last cached version of this calendar")
        box.exec_()

    def getCurrentSeriesOfSeminar(self, seminarName):
        return DomainFactorySingleton().createDomainByName(seminarName).getCurrentSeries()

    def getEventUIDFromName(self, eventName):
        for event in self.events:
            if eventName == event.summary:
                return event.uid

    def getEventFromUID(self, uid):
        for event in self.events:
            if uid == event.uid:
                return event

    def makeEventInterested(self, event, notifyHoursBefore):
        event.interested = True
        event.notifyBeforeHours = notifyHoursBefore

    def getEvents(self):
        return self.events
