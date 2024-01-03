from PyQt5.QtWidgets import QTabWidget, QScrollArea

from CubedCalendar.CalendarUI import CubedCalendar
from FileStructure.FileStructure import FileStructure
from SeminarOverview.SeminarOverviewTab import SeminarOverviewTab


class SideBar(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setTabsClosable(False)

        self.scrollarea = QScrollArea()
        self.calendar = CubedCalendar()
        self.scrollarea.setWidget(self.calendar)

        self.filestructure = FileStructure()

        self.seminarOverview = SeminarOverviewTab()

        self.addTab(self.scrollarea, "Calendar")
        self.addTab(self.filestructure,"File Structure")
        self.addTab(self.seminarOverview, "Overview")
    def addTab(self, widget, a1):
        super().addTab(widget,a1)
