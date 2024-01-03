from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout, QComboBox, QPushButton, QWidget

from CubedCalendar.CalendarModel import CalendarModel
from CubedCalendar.EventLabel import EventLabel


class CalendarEventDialog(QDialog):
    @staticmethod
    def getNotifyMeItemsList():
        return ["1d", "2d", "5d", "1w", "2w"]

    @staticmethod
    def getHoursFromItem(index):
        itemDeltaDict = {
            "1d": 24,
            "2d": 48,
            "5d": 24 * 5,
            "1w": 24 * 7,
            "2w": 24 * 14
        }
        return itemDeltaDict[index]

    def __init__(self, calendarEvent):
        super().__init__()
        self.calendarEvent = calendarEvent
        self.layout = QVBoxLayout()

        self.titleLabel = QLabel(self.calendarEvent.summary)
        self.titleLabel.setAlignment(Qt.AlignHCenter)
        self.info = QLabel(f"Od:{self.calendarEvent.start}\n"
                           f"Do:{self.calendarEvent.end}")

        self.isInterested = QCheckBox("I am interested in this event")

        self.notifyMeLayout = QHBoxLayout()
        self.notifyMeLabel = QLabel("Notify me in:")
        self.notifyMeDropdown = QComboBox()
        self.notifyMeDropdown.addItems(CalendarEventDialog.getNotifyMeItemsList())

        self.notifyMeLayout.addWidget(self.notifyMeLabel)
        self.notifyMeLayout.addWidget(self.notifyMeDropdown)

        self.okButton = QPushButton("Ok")
        self.okButton.clicked.connect(self.close)

        self.layout.addWidget(self.titleLabel)
        self.layout.addWidget(self.info)
        self.layout.addWidget(self.isInterested)
        self.layout.addLayout(self.notifyMeLayout)
        self.layout.addWidget(self.okButton)
        self.setLayout(self.layout)

    def close(self):
        super().close()
        checked = self.isInterested.isChecked()
        self.setResult(self.notifyMeDropdown.currentIndex() if checked else -1)


class CubedCalendar(QWidget):
    def __init__(self):
        super().__init__()
        self.model = CalendarModel()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.model.load()
        self.generate()

    def generate(self):
        for event in self.model.events:
            label = EventLabel(event)
            label.clicked.connect(self.onLabelClicked)
            if event.interested:
                label.makeImportant()
            self.layout.addWidget(label)

    def onLabelClicked(self, label: EventLabel) -> None:
        box = CalendarEventDialog(label.getEvent())
        index = box.exec()
        if index == -1:
            label.getEvent().interested = False
            label.makeUnimportant()
            return
        item = CalendarEventDialog.getNotifyMeItemsList()[index]
        hours = CalendarEventDialog.getHoursFromItem(item)

        self.model.makeEventInterested(label.getEvent(), hours)
        label.makeImportant()
