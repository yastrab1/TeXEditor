from PyQt5.QtWidgets import QTabWidget, QScrollArea

from CubedCalendar.CalendarModel import CubedCalendar
from FileStructure.FileStructure import FileStructure


class SideBar(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(False)

        self.scrollarea = QScrollArea()
        self.calendar = CubedCalendar()
        self.scrollarea.setWidget(self.calendar)

        self.filestructure = FileStructure()

        self.addTab(self.scrollarea, "Calendar")
        self.addTab(self.filestructure,"File Structure")
    def addTab(self, widget, a1):
        super().addTab(widget,a1)
