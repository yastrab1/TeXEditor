from PyQt5.QtWidgets import QFrame, QVBoxLayout, QPushButton

from Domains.WebDrivers.RieskyDriver import RieskyDriver


class SeminarOverviewTab(QFrame):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.testButton = QPushButton("Work in progress")

        self.layout.addWidget(self.testButton)

        self.testButton.clicked.connect(self.submitFile)
        self.setLayout(self.layout)

    def submitFile(self):
        page = RieskyDriver()
        page.authenticate()
        page.submitFile(r"C:\Users\dc\PycharmProjects\TeXEditor\FileSystem\Pikofyz\1._séria\1._úloha.pdf",
                        26, 3, 6)
