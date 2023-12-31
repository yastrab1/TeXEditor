from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton

from SeminarPage.RieskyPage import RieskyScraper


class SeminarOverviewTab(QFrame):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.testButton = QPushButton("Work in progress")

        self.layout.addWidget(self.testButton)

        self.testButton.clicked.connect(lambda: print(RieskyScraper().getPointsFromSeries(3, 26)))
        self.setLayout(self.layout)
