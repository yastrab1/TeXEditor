from PyQt5.QtWidgets import QTabWidget, QScrollArea

from CubedCalendar.CalendarUI import CubedCalendar
from FileStructure.FileStructure import FileStructure
from PdfViewer.PdfViewer import PdfViewer
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

        self.pdfViewer = PdfViewer()

        self.addTab(self.scrollarea, "Calendar")
        self.addTab(self.filestructure,"File Structure")
        self.addTab(self.seminarOverview, "Overview")
        self.addTab(self.pdfViewer, "Pdf Viewer")
    def addTab(self, widget, a1):
        super().addTab(widget,a1)

    def openPdf(self, url):
        self.pdfViewer.openPdf(url)
        self.setCurrentIndex(3)
